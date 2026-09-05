import cv2
from core.logger import create_logger
import os

logger = create_logger("CAMERA")

class CameraEngine:
    def __init__(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                logger.warning("Camera not available")
                self.camera = None
            else:
                logger.info("Camera initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            self.camera = None
    
    def take_photo(self, filename="data/photos/photo.jpg"):
        """عکس بگیر"""
        try:
            if not self.camera or not self.camera.isOpened():
                logger.error("Camera not available")
                return False
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            ret, frame = self.camera.read()
            if ret:
                cv2.imwrite(filename, frame)
                logger.info(f"Photo taken: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error taking photo: {e}")
            return False
    
    def start_stream(self, window_name="JARVIS Camera"):
        """نمایش زنده دوربین"""
        try:
            if not self.camera or not self.camera.isOpened():
                logger.error("Camera not available")
                return False
            
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                
                cv2.imshow(window_name, frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            logger.error(f"Error in camera stream: {e}")
            return False
    
    def close(self):
        """بستن دوربین"""
        try:
            if self.camera:
                self.camera.release()
                cv2.destroyAllWindows()
        except Exception as e:
            logger.error(f"Error closing camera: {e}")
