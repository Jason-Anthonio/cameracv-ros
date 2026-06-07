# TO CHANGE THE IMAGE PROCESSING COLOR, SET THE 'color' PARAMETER TO 'red' OR 'blue'
# You can use the YAML file to set before launching

# You can also change parameter during runtime using ROS2 param set command:
# ros2 param set /camera_subscriber color red or blue

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraSubscriber(Node):
    def __init__(self):

        super().__init__('camera_subscriber')

        self.subscription = self.create_subscription(
            Image,
            'camframes',
            self.listener_callback,
            10)
        
        self.subscription
        self.bridge = CvBridge()

        self.red_lower = np.array([136, 87, 111], np.uint8)
        self.red_upper = np.array([180, 255, 255], np.uint8)
        self.blue_lower = np.array([94, 80, 2], np.uint8)
        self.blue_upper = np.array([126, 255, 255], np.uint8)

        self.kernal = np.ones((5, 5), "uint8")
        
        try:
            cv2.namedWindow("camera_publisher", cv2.WINDOW_NORMAL)

        except Exception:
            pass
        
        self.declare_parameter('color', 'red')



    def listener_callback(self, msg):
        self.get_logger().info('Received frame at time: "%s"' % msg.header.stamp)

        self.color = self.get_parameter('color').get_parameter_value().string_value

        param_color = self.color

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        except Exception:
            arr = np.frombuffer(msg.data, dtype=np.uint8)
            try:
                frame = arr.reshape((msg.height, msg.width, -1))
            except Exception:
                frame = arr

        if param_color == 'red':
            frame = detect_red_objects(frame, self.red_lower, self.red_upper, self.kernal)
        elif param_color == 'blue':
            frame = detect_blue_objects(frame, self.blue_lower, self.blue_upper, self.kernal)
        else:
            self.get_logger().warning(f"Unknown color parameter '{param_color}', using red as default")
            frame = detect_red_objects(frame, self.red_lower, self.red_upper, self.kernal)

        cv2.imshow("camera_publisher", frame)

        try:
            cv2.waitKey(1)
        except Exception:
            pass
    

    def destroy_node(self):
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
        return super().destroy_node()
    
    
def detect_red_objects(frame, red_lower, red_upper, kernal):
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsvframe, red_lower, red_upper)
    red_mask = cv2.dilate(red_mask, kernal)
    
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y),
                                    (x + w, y + h),
                                    (0, 0, 255), 2)

            cv2.putText(frame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))
    return frame

def detect_blue_objects(frame, blue_lower, blue_upper, kernal):
    hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsvframe, blue_lower, blue_upper)
    blue_mask = cv2.dilate(blue_mask, kernal)
    
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)

            cv2.putText(frame, "Blue Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (255, 0, 0))
    return frame

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriber()
    try:
        rclpy.spin(camera_subscriber)
    finally:
        camera_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()