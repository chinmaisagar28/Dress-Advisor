from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import imutils
import pprint
import base64
from flask_session import Session


# app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = '847b3d461d046d54bdf129bff2054368f292ec1347b9a5e7'

# Increase the maximum cookie size limit in Flask application configuration
app.config['MAX_COOKIE_SIZE'] = 8192   # Set to a higher value as needed
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the server-side
app.config['SESSION_FILE_DIR'] = 'static/session-storage'  # Directory to store session files
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Ensure session cookie is HTTP only

Session(app)

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in an image
def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def extractSkin(image):
    # Taking a copy of the image
    img = image.copy()
    # Converting from BGR Colours Space to HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Defining HSV Threadholds
    lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    upper_threshold = np.array([20, 255, 255], dtype=np.uint8)

    # Single Channel mask,denoting presence of colours in the about threshold
    skinMask = cv2.inRange(img, lower_threshold, upper_threshold)

    # Cleaning up mask using Gaussian Filter
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

    # Extracting skin from the threshold mask
    skin = cv2.bitwise_and(img, img, mask=skinMask)

    # Return the Skin image
    return cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)

def removeBlack(estimator_labels, estimator_cluster):
    # Check for black
    hasBlack = False

    # Get the total number of occurance for each color
    occurance_counter = Counter(estimator_labels)

    # Quick lambda function to compare to lists
    def compare(x, y): return Counter(x) == Counter(y)

    # Loop through the most common occuring color
    for x in occurance_counter.most_common(len(estimator_cluster)):

        # Quick List comprehension to convert each of RBG Numbers to int
        color = [int(i) for i in estimator_cluster[x[0]].tolist()]

        # Check if the color is [0,0,0] that if it is black
        if compare(color, [0, 0, 0]) == True:
            # delete the occurance
            del occurance_counter[x[0]]
            # remove the cluster
            hasBlack = True
            estimator_cluster = np.delete(estimator_cluster, x[0], 0)
            break

    return (occurance_counter, estimator_cluster, hasBlack)

def getColorInformation(estimator_labels, estimator_cluster, hasThresholding=False):
    # Variable to keep count of the occurance of each color predicted
    occurance_counter = None

    # Output list variable to return
    colorInformation = []

    # Check for Black
    hasBlack = False

    # If a mask has be applied, remove th black
    if hasThresholding == True:

        (occurance, cluster, black) = removeBlack(
            estimator_labels, estimator_cluster)
        occurance_counter = occurance
        estimator_cluster = cluster
        hasBlack = black

    else:
        occurance_counter = Counter(estimator_labels)

    # Get the total sum of all the predicted occurances
    totalOccurance = sum(occurance_counter.values())

    # Loop through all the predicted colors
    for x in occurance_counter.most_common(len(estimator_cluster)):

        index = (int(x[0]))

        # Quick fix for index out of bound when there is no threshold
        index = (index-1) if ((hasThresholding & hasBlack)
                              & (int(index) != 0)) else index

        # Get the color number into a list
        color = estimator_cluster[index].tolist()

        # Get the percentage of each color
        color_percentage = (x[1]/totalOccurance)

        # make the dictionay of the information
        colorInfo = {"cluster_index": index, "color": color,
                     "color_percentage": color_percentage}

        # Add the dictionary to the list
        colorInformation.append(colorInfo)

    return colorInformation


def extractDominantColor(image, number_of_colors=2, hasThresholding=False):
    # Quick Fix Increase cluster counter to neglect the black(Read Article)
    if hasThresholding == True:
        number_of_colors += 1

    # Taking Copy of the image
    img = image.copy()

    # Convert Image into RGB Colours Space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape Image
    img = img.reshape((img.shape[0]*img.shape[1]), 3)

    # Initiate KMeans Object
    estimator = KMeans(n_clusters=number_of_colors, random_state=0, n_init=10)

    # Fit the image
    estimator.fit(img)

    # Get Colour Information
    colorInformation = getColorInformation(
        estimator.labels_, estimator.cluster_centers_, hasThresholding)
    
    # Find the highest RGB values
    highestRed = max(color[0] for color in estimator.cluster_centers_)
    highestGreen = max(color[1] for color in estimator.cluster_centers_)
    highestBlue = max(color[2] for color in estimator.cluster_centers_)
    
    # Add highest RGB values to the dominantColors list
    dominantColors = [{'cluster_index': -1, 'color': [highestRed, highestGreen, highestBlue], 'color_percentage': 0}] + colorInformation
    
    return dominantColors


def pretty_print_data(color_info):
    for x in color_info:
        print(pprint.pformat(x))
        print()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get uploaded image file 
            image_file = request.files['file']

            # Check file size
            max_file_size = 2 * 1024 * 1024  # 2MB
            if image_file and image_file.content_length > max_file_size:
                session['error_message'] = 'File size exceeds the maximum limit of 2MB.'
                return redirect(url_for('error'))
            
            # Read the image file
            image_data = image_file.read()
            if not image_data:
                session['error_message'] = 'Unable to read the image file.'
                return redirect(url_for('error'))
            
            # Decode image data
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                session['error_message'] = 'Unable to decode the image file. Please try with different File format!'
                return redirect(url_for('error'))

            # Resize image to a width of 250
            image = imutils.resize(image, width=550)

            # Detect faces in the uploaded image
            faces = detect_faces(image)

            # If no faces detected or multiple faces detected, render error message 
            if len(faces) == 0:
                session['error_message'] = 'No faces detected in the uploaded image.'
                return redirect(url_for('error'))
            elif len(faces) >= 2:
                session['error_message'] = 'Multiple Faces Detected'
                return redirect(url_for('error'))

            # Draw rectangles around detected faces
            # draw_faces(image, faces)

            # Extract skin from the detected face region
            for (x, y, w, h) in faces:
                face_region = image[y:y+h, x:x+w]
                skin = extractSkin(face_region)

                # Find the dominant color in the skin region
                dominantColors = extractDominantColor(skin, hasThresholding=True)

                for color in dominantColors:
                    color['color'] = [int(val) for val in color['color']]

                # Encode images to base64
                _, skin_encoded = cv2.imencode('.jpg', skin)
                skin_base64 = base64.b64encode(skin_encoded).decode('utf-8')

                # Encode the original image to base64
                _, image_encoded = cv2.imencode('.jpg', image)
                image_base64 = base64.b64encode(image_encoded).decode('utf-8')

                # Store image and other data in session for rendering result template
                session['image_base64'] = image_base64
                session['skin_base64'] = skin_base64
                session['dominant_colors'] = dominantColors

                # Redirect to the result page
                return redirect(url_for('result'))
        except Exception as e:
            # Handle exceptions
            session['error_message'] = f"An error occurred: {str(e)}. Please try again with a different image file."
            return redirect(url_for('error'))
    
    # Render the upload form in HTML template
    return render_template('upload.html')

@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'GET':
        try:
            error_message = session.pop('error_message', None)
            if error_message:
                return render_template('error.html', error_message=error_message)
        except Exception:
                return redirect(url_for('/'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    image_base64 = session.pop('image_base64', None)
    skin_base64 = session.pop('skin_base64', None)
    dominant_colors = session.pop('dominant_colors', None)

    if image_base64 and skin_base64 and dominant_colors:
        return render_template('result.html', image=image_base64, skin=skin_base64, dominantColors=dominant_colors)
    else:
        session['error_message'] = 'An error occurred while processing image. Please try again.'
        return redirect(url_for('error'))
    
@app.route('/navPages/about')
def about():
    return render_template('navPages/about.html')

@app.route('/navPages/contact')
def contact():
    return render_template('navPages/contact.html')
    
if __name__ == '__main__':
    app.run(debug=True)