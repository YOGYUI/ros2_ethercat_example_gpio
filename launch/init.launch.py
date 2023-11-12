import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    package_name = 'ros2_ethercat_example_gpio'
    xacro_file_name = 'robot.urdf.xacro'
    xacro_file_path = os.path.join(
        get_package_share_directory(package_name),
        'description/' + xacro_file_name
    )
    doc = xacro.process_file(xacro_file_path)
    robot_desc = doc.toprettyxml(indent='  ')
    ros2_control_cfg_path = os.path.join(
        get_package_share_directory(package_name),
        'config/ros2_controllers.yaml'
    )
    
    ld = LaunchDescription()
    ld.add_action(DeclareLaunchArgument("publish_frequency", default_value="1000.0"))

    # ros2 control node
    ros2_control_node = Node(
        package="controller_manager", 
        executable="ros2_control_node", 
        parameters=[
            {'robot_description': robot_desc},
            ros2_control_cfg_path
        ]
    )
    ld.add_action(ros2_control_node)

    # spawn controllers node
    controller_names = [
        "gpio_controller"
    ]
    for name in controller_names:
        node = Node(
            package="controller_manager",
            executable="spawner",
            arguments=[name],
            output="screen"
        )
        ld.add_action(node)

    return ld