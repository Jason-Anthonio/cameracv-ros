import sys

from cameracv_interfaces.srv import Capture
import rclpy
from rclpy.node import Node


class CameraClientAsync(Node):

    def __init__(self):
        super().__init__('camera_client_async')

        self.cli = self.create_client(Capture, 'capture')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        self.req = Capture.Request()

    def send_request(self, iterations):
        self.req.iterations = iterations
        return self.cli.call_async(self.req)
        


def main():
    rclpy.init()
    count = int(sys.argv[1])

    camera_client = CameraClientAsync()

    future = camera_client.send_request(count)

    rclpy.spin_until_future_complete(camera_client, future)

    response = future.result()

    if response.success:
        camera_client.get_logger().info(
            'The service response: %d times has run' %
            (count))

    camera_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()