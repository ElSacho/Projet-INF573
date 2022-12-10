import cv2

# Charger la vidéo
cap = cv2.VideoCapture(0)

# Lire les frames de la vidéo
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # Convertir la frame en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Appliquer un seuil sur les niveaux de gris
        thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

        # Afficher la frame modifiée
        cv2.imshow('Frame', thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
