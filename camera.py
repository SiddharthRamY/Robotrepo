import cv2
import torch

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Load YOLOv5s model from Ultralytics (first time will download weights)
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
        # YOLOv5 expects RGB images
        results = self.model(frame)
        # Annotate the frame with detections
        annotated_frame = results.render()[0]
        ret, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()
