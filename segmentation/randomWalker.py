import numpy as np
import cv2
import math 
import scipy

def matrix_to_vector(matrice):
    return matrice.flatten()

def fonction_weight(gi,gj, beta):
    return math.exp(-beta*math.dist(gi,gj)*math.dist(gi,gj))

def get_matrice_L(matrice,beta):
    
    #Initialisation de la matrice finale avec des zeros partout
    nx, ny , nz = matrice.shape
    L = np.zeros((nx*ny,nx*ny))
    
    # on remplit les points qui doivent l'être
    for i in range(nx):
        for j in range(ny):
            
            valeurCentrale=0
            
            # On prend tous les voisins, potentielle optimisation ici car on calcul plusieurs fois les mêmes valeurs, 
            # les poids étant symetriques
            
            for nex,ney in neighboor_all(i,j,ny,nx):
                
                weight = - fonction_weight(matrice[i,j],matrice[nex,ney], beta)
                valeurCentrale+=weight
                id1 = i*ny+j
                id2 = nex*ny+ney
                
                #Comme la matrice est symétrique on peut ajoute les valeurs aux deux endroits directement
                
                L[id1,id2] = weight
                L[id2,id1] = weight
                
            # On ajoute la somme des poids avec les voisins pour le point central
            L[i*ny+j,i*ny+j] = - valeurCentrale
            
    return L   

def neighboor_all(i,j, ny, nx):
    
    neighboor =[]
    list_idx = [ i - k + 1 for k in range(3) if (i - k + 1 >= 0 and i - k + 1 <= nx - 1 ) ]
    list_idy = [ j - k + 1 for k in range(3) if (j - k + 1 >= 0 and j - k + 1 <= ny - 1 ) ]
    
    for idx in list_idx:
        for idy in list_idy:
            neighboor.append([idx, idy])
            
    return neighboor    
  
def get_permutation(vector_label, nbr_points_labelises):
    
    idx_label = 0
    pointeurActuel = 0
    tabPermutation = []
    # tant qu'on a pas mis tous les labels devant
    while idx_label < nbr_points_labelises or pointeurActuel<len(vector_label):
        
        # Si on est pas labelise va voir le points suivants
        if vector_label[ pointeurActuel ] == 0:
            pointeurActuel += 1
            
        else :
            #On echange les les valeurs entre le premier point non labelise et le point labelise
            temp = vector_label[ pointeurActuel ]
            vector_label[ pointeurActuel ] = vector_label[ idx_label ]
            vector_label[ idx_label ] = temp
            
            #On ajoute la permutation dans le tableau et augmente le nombre de labels presents dans la nouvelle liste
            tabPermutation.append([pointeurActuel,idx_label])
            idx_label += 1
            
    return tabPermutation, vector_label

def getMatricePermutation(IDE,perm):
    #pour tous les echanges a faire on effectue l'echange
    for echange in perm:
        depart = echange[0]
        arrivee = echange[1]
        temp = IDE[:,depart].copy()
        IDE[:,depart] = IDE[:,arrivee]
        IDE[:,arrivee] = temp
        
    return IDE

def permuteL(L,perm):
    #On trouve la premiere matrice de permutation
    id =  np. eye(L.shape[0])
    P1 = getMatricePermutation(id,perm)

    # On trouve la seconde matrice de permutation
    id2 = np. eye(L.shape[0]) 
    P2 = getMatricePermutation(id2,perm[::-1])

    #On effectue le calcul
    #C'est la phase la plus longue de l'algorithme
    return P1@L@P2
        
def getMatricesToSolve(L,vectorLabelOrdone,nbr_points_labelises,nbrLabels ):
    # On extrait Lu et B de L
    Lu = L[nbr_points_labelises:,nbr_points_labelises:]
    B = L[:nbr_points_labelises:, nbr_points_labelises:]
    
    M = np.zeros((nbr_points_labelises,nbrLabels))
    
    i = 0
    while i<len(vectorLabelOrdone) and vectorLabelOrdone[i]!=0:
        k = int(vectorLabelOrdone[i])
        M[i,k-1]=1
        i+=1
    
    return Lu, B, M

def solve(Lu, B, xM):
    xU = - np.linalg.inv(Lu) @ B.T @xM
    return xU

def solve2(Lu,B,M):
    K = M.shape[1]
    xU=[]
    for idx in range(K):
            pot = scipy.sparse.linalg.spsolve(
                Lu, -B.T @ M[:,idx])
            xU.append(pot)
    return xU

def permutationVecteur(x, perm):

    #Pour toutes les permutations on echange de place les deux donnees
    for echange in perm:
        depart = echange[0]
        arrivee = echange[1]
        
        temp = x[depart].copy()
        x[depart] = x[arrivee]
        x[arrivee] = temp
        
    return x

def transformEnLabel(M,xu):
    x = []
    
    # On parcourt M pour applatir obtenir un vecteur avec le numéro du label a tous les endroits
    for el in M:
        idx = 0
        for val in el:
            if val==1:
                x.append(idx+1)
                break
            idx+=1
            
    # On parcourt xu pour trouver la segmentation la plus probable selon l'algorithme
    for el in xu:
        idx = 0
        m = el[0]
        for k in range(1,len(el)):
            if el[k]>m:
                idx = k
        x.append(idx+1)
        
    return np.array(x)

def resize_vector_to_matrix(x, img):
    nx, ny, nz = img.shape
    return x.reshape((nx,ny))

def random_walk(img, matrice_label, nbr_points_labelises ,nbrLabels ,beta=10):
    
    # On construit la matrice L
    L = get_matrice_L(img/255,beta)
    
    # On permute cette matrice pour placer les vecteurs labelises devant
    vector_labelise = matrix_to_vector(matrice_label)
    perm, vectorLabelise_ordonne = get_permutation(vector_labelise, nbr_points_labelises)
    L = permuteL(L,perm)

    # On extrait les matrices necessaires a la resolution de l'equation
    Lu , B , M = getMatricesToSolve(L,vectorLabelise_ordonne,nbr_points_labelises, nbrLabels)

    # On resout le systeme pour obtenir la matrice des probabilites d'appartenir a chaque label
    # Essayer de modifier cette fonction solve pour aller plus vite surtout pour des dimensions plus grandes
    xu = solve(Lu, B, M)
    
    # On reorganise les resultats en transformant les probabilites en labelisation 
    # et reorganise les resultats dans l'ordre
    x = transformEnLabel(M,xu)
    x = permutationVecteur(x, perm[::-1])
    imgLabel = resize_vector_to_matrix(x, img)
    
    # On renvoit un array de la taille de l'image à labeliser ou toutes les valeurs sont le label 
    # auquel les points appartiennent probablement
    return imgLabel
