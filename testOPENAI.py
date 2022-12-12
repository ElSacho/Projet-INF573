# Import des bibliothèques nécessaires
import cv2

# Ouvre la webcam
webcam = cv2.VideoCapture(0)

# Boucle infinie pour afficher la vidéo en temps réel
while True:
    # Capture une image à partir de la webcam
    _, frame = webcam.read()

    # Transforme l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détermine les dimensions de l'image
    height, width = gray.shape

    # Détermine les coordonnées du rectangle de 100qqx100 pixels au centre de l'image
    start_x = int(width / 2 - 50)
    start_y = int(height / 2 - 50)
    end_x = int(width / 2 + 50)
    end_y = int(height / 2 + 50)

    # Dessine un rectangle de 100x100 pixels au centre de l'image en noir
    cv2.rectangle(gray, (start_x, start_y), (end_x, end_y), (0, 0, 0), thickness=2)

    # Affiche l'image en noir et blanc avec un rectangle de 100x100 pixels au centre
    cv2.imshow("Webcam", gray)

    # Si l'utilisateur appuie sur la touche "q", quitte la boucle infinie
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Ferme la fenêtre et libère les ressources utilisées par la webcam
webcam.release()
cv2.destroyAllWindows()
