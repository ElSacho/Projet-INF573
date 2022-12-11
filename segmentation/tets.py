import cv2

# Charger l'image
img = cv2.imread("segmentation/assets/tete.jpg")

# Créer une fenêtre avec la taille souhaitée
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 600, 600)

# Naming a window
cv2.namedWindow("Resize", cv2.WINDOW_NORMAL)
  
  
# Using resizeWindow()
cv2.resizeWindow("Resize", 700, 200)
  
# Displaying the image
cv2.imshow("Resize", img)
# Afficher l'image dans la fenêtre
cv2.imshow("image", img)

# Attendre que l'utilisateur appuie sur une touche pour fermer la fenêtre
cv2.waitKey(0)