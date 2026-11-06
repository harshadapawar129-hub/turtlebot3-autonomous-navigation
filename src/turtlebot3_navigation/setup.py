from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'turtlebot3_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),
        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='harshada',
    maintainer_email='harshadapawar129@gmail.com',
    description='Autonomous TurtleBot3 navigation using ROS 2 Jazzy, Gazebo, SLAM Toolbox, Nav2 and sequential waypoint execution',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'waypoint_navigator = turtlebot3_navigation.waypoint_navigator:main',
    ],
  },
)
