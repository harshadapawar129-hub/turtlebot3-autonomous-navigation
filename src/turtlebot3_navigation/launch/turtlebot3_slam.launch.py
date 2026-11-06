from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Locate Gazebo package
    gazebo_dir = get_package_share_directory('turtlebot3_gazebo')

    # Locate SLAM Toolbox package
    slam_dir = get_package_share_directory('slam_toolbox')

    # Launch Gazebo world
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_dir, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    # Launch SLAM Toolbox
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_dir, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'True'
        }.items()
    )

    # Launch RViz2
    rviz_config = os.path.join(
    get_package_share_directory('turtlebot3_navigation'),
    'rviz',
    'turtlebot3_slam.rviz'
    )

    rviz_node = Node(
       package='rviz2',
       executable='rviz2',
       name='rviz2',
       arguments=['-d', rviz_config],
       output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        slam_launch,
        rviz_node
    ])
