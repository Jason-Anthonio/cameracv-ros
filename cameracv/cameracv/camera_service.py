import rclpy
from rclpy.node import Node

import cv2
from cameracv_interfaces.srv import Capture

class CameraService(Node):
    def __init__(self):
        super().__init__('camera_service')
        self.srv = self.create_service(Capture, 'capture', self.capture_callback)

    def capture_callback(self, request, response):
        self.get_logger().info('Incoming request: %d times' % (request.iterations))

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            response.success = False
            self.get_logger().info('Failed to open camera')
            return response

        captured = 0
        for i in range(request.iterations):
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().info('Failed to read from camera')
                break

            filename = f'capture_{i}.png'
            cv2.imwrite(filename, frame)
            self.get_logger().info(f'Captured and saved {filename}')
            captured += 1

        response.success = (captured == request.iterations)
        if response.success:
            self.get_logger().info('Service finished successfully')
        else:
            self.get_logger().info('Service incomplete or failed')

        return response
    

    def destroy_node(self):
        try:
            if hasattr(self, 'cap') and self.cap is not None:
                try:
                    if self.cap.isOpened():
                        self.cap.release()
                except Exception:
                    pass
        finally:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass
            return super().destroy_node()


def main():
    rclpy.init()

    camera_service = CameraService()

    try:
        rclpy.spin(camera_service)
    finally:
        camera_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()