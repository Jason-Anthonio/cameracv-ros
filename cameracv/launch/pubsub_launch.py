from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    config_file = os.path.join(
        os.path.dirname(__file__), '..', 'config','color_params.yaml'
    )

    if not os.path.exists(config_file):
        print(f"[ERROR] YAML file not found: {config_file}")

    return LaunchDescription([

        Node(
            package='cameracv',
            executable='camera_publisher',
            name='camera_publisher',
            output='screen'
        ),

        Node(
            package='cameracv',
            executable='camera_subscriber',
            name='camera_subscriber',
            output='screen',
            parameters=[config_file]  # Load YAML parameters
        ),
    ])