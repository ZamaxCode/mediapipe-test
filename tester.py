# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

model = 'exported_model/gesture_recognizer.task'

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


cap = cv2.VideoCapture(0)

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))
    cv2.imshow('Custom Model Output', output_image)

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with GestureRecognizer.create_from_options(options) as recognizer:
    cap = cv2.VideoCapture(0)
    timestamp = 1
    while True:
        _, frame = cap.read()

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(mp_image, timestamp)
        timestamp+=1

        #cv2.imshow('Custom Model Output', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
