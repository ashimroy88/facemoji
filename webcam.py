from cv2 import WINDOW_NORMAL
from face_detect import find_faces, normalize_face
from image_commons import nparray_as_image, image_as_nparray, draw_with_alpha

def load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    :param emotions: Array of emotions names.
    :return: Array of emotions graphics.
    """
    return [nparray_as_image(cv2.imread('graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]

def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    :param model: Learnt emotion detection model.
    :param emoticons: List of emotions images.
    :param window_size: Size of webcam image window.
    :param window_name: Name of webcam image window.
    :param update_time: Image update time interval.
    """
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()
    else:
        print("webcam not found")
        return

    while read_value:
        faces_coordinates = find_faces(webcam_image)

        for (x, y, w, h) in faces_coordinates:
            normalized_face = normalize_face(frame[y:y + h, x:x + w])
            prediction = model.predict(normalized_face)
            image_to_draw = emoticons[prediction[0]]
            
            draw_with_alpha(webcam_image, image_to_draw, x, y, w, h)
        
        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)
        
        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow(window_name)

if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = load_emoticons(emotions)

    # load model
    if cv2.__version__ == '3.1.0':
        fisher_face = cv2.face.createFisherFaceRecognizer()
    else:
        fisher_face = cv2.createFisherFaceRecognizer()
    fisher_face.load('models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'WEBCAM (press ESC to exit)'
    show_webcam_and_run(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)