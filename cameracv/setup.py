import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'cameracv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jason-anthonio',
    maintainer_email='jason-anthonio@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_publisher = cameracv.camera_publisher:main',
            'camera_subscriber = cameracv.camera_subscriber:main',
            'camera_service = cameracv.camera_service:main',
            'camera_client = cameracv.camera_client:main',
        ],
    },
)
