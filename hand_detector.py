import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model = 'exported_model/hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
with HandLandmarker.create_from_options(options) as landmarker:

    cap = cv2.VideoCapture(0)
    timestamp=1
    while True:
        _, frame = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        landmarker.detect_async(mp_image, timestamp)
        timestamp+=1
        
        cv2.imshow('Custom Model Output', annotated_image, cv2.COLOR_RGB2BGR)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()