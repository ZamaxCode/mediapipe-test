# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2


# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='exported_model/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    recognition_result = recognizer.recognize(mp_image)
    try:
        top_gesture = recognition_result.gestures[0][0]
    except:
        pass
    hand_landmarks = recognition_result.hand_landmarks
    print(recognition_result.gestures)
    cv2.imshow('Custom Model Output', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
