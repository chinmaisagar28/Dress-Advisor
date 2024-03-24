import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Load face cascade classifier
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(img):
    """
    Detect faces in the input image using the Haar cascade classifier.

    Parameters:
    - img: Input image in BGR format.

    Returns:
    - faces: A list of tuples representing the bounding boxes of detected faces (x, y, w, h).
    """
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=1, minSize=(40, 40))
    # faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def crop_faces(img, faces):
    """
    Crop faces from the input image based on the detected bounding boxes.

    Parameters:
    - img: Input image in BGR format.
    - faces: List of tuples representing the bounding boxes of detected faces.

    Returns:
    - cropped_faces: List of cropped face images.
    """
    cropped_faces = []
    for (x, y, w, h) in faces:
        cropped = img[y:y+h, x:x+w]
        cropped_faces.append(cropped)
    return cropped_faces

def visualize_faces(img, faces):
    """
    Visualize the detected faces on the input image.

    Parameters:
    - img: Input image in BGR format.
    - faces: List of tuples representing the bounding boxes of detected faces.
    """
    img_copy = img.copy()
    for (x, y, w, h) in faces:
        cv.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)
    plt.imshow(cv.cvtColor(img_copy, cv.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Load the input image
image_path = r'c:\Users\chinnu\Downloads\sah.jpg'
image = cv.imread(image_path)

# Check if image is loaded successfully
if image is None:
    print("Error: Unable to load image.")
else:
    # Detect faces in the image
    faces = detect_faces(image)

    # Check if any faces are detected
    if len(faces) == 0:
        print("No faces detected in the image.")
    else:
        # Visualize the detected faces on the original image
        visualize_faces(image, faces)

        # Crop the faces from the image
        cropped_faces = crop_faces(image, faces)

        # Visualize the cropped faces
        for i, face in enumerate(cropped_faces):
            plt.subplot(1, len(cropped_faces), i+1)
            plt.imshow(cv.cvtColor(face, cv.COLOR_BGR2RGB))
            plt.axis('off')
        plt.show()
