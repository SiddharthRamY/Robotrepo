import cv2
import torch
import datetime
import os

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.conf_threshold = 0.25  # Default confidence threshold

    def __del__(self):
        self.video.release()

    def set_confidence_threshold(self, threshold):
        self.conf_threshold = threshold

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None

        # Run object detection
        results = self.model(frame)
        detections = results.pandas().xyxy[0]

        # Filter by confidence threshold
        filtered = detections[detections['confidence'] >= self.conf_threshold]

        # Draw boxes
        for _, row in filtered.iterrows():
            x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
            label = f"{row['name']} {row['confidence']:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode to JPEG for Flask
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def capture_screenshot(self):
        success, frame = self.video.read()
        if not success:
            return None

        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.jpg"
        filepath = os.path.join("screenshots", filename)

        cv2.imwrite(filepath, frame)
        print(f"📸 Screenshot saved: {filepath}")
        return filename
