import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np

class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')
        self.cap = cv2.VideoCapture(0)
        self.publisher_ = self.create_publisher(Image, 'camframes', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0   

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = Image()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.height = frame.shape[0]
            msg.width = frame.shape[1]
            msg.encoding = 'bgr8'
            msg.is_bigendian = False
            msg.step = frame.strides[0]
            msg.data = np.array(frame).tobytes()
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing frame {self.i}')
            self.i += 1
    
    def destroy_node(self):
        """Release camera and destroy OpenCV windows before destroying the node."""
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
        



def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    try:
        rclpy.spin(camera_publisher)
    finally:
        camera_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()