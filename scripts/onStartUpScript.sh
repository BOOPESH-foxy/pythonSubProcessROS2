#!/bin/zsh
source /opt/ros/humble/setup.zsh
source /home/roots/PythonRos2_scripting/install/setup.zsh
echo "Starting ROS 2 nodes..."
ros2 run service_talker talker_trigger_node