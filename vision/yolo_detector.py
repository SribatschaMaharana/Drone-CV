from ultralytics import YOLO
import cv2
import os

class YOLODetector:
    def __init__(self, model_path=None, conf_threshold=0.5):
        if model_path is None:
            # ABSOLUTE path to model
            here = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(here, "assets", "yolov8n.pt")

        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        print(f"[INFO] Using YOLO model from: {model_path}")
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model.predict(source=frame, conf=self.conf_threshold, verbose=False)
        annotated_frame = frame.copy()

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = self.model.names[cls]

                # bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return annotated_frame
