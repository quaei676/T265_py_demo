# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
import pyrealsense2 as rs

class Talker(Node):

    def __init__(self):
        super().__init__('realsense_odom')
        self.i = 0
        self.pub = self.create_publisher(Odometry, 'T265_odom')
        pipe = rs.pipeline()
        timer_period = 1.0
        cfg = rs.config()
        cfg.enable_stream(rs.stream.pose)
        pipe.start(cfg)
        odom = Odometry()
        self.get_logger().info('Start Pose track')
        while(1):
            # Wait for the next set of frames from the camera
            frames = pipe.wait_for_frames()

            # Fetch pose frame
            pose = frames.get_pose_frame()
            if pose:
                # Print some of the pose data to the terminal
                pose = frames.get_pose_frame()
                data = pose.get_pose_data()
                odom.header.frame_id = "odom"
                odom.pose.pose.position.x=-data.translation.z
                odom.pose.pose.position.y=-data.translation.x
                odom.pose.pose.position.z=data.translation.y
                odom.twist.twist.linear.x=-data.velocity.z
                odom.twist.twist.linear.y=-data.velocity.x
                odom.twist.twist.linear.z=data.velocity.y
                odom.pose.pose.orientation.x=data.rotation.x
                odom.pose.pose.orientation.y=data.rotation.y
                odom.pose.pose.orientation.z=data.rotation.z
                odom.pose.pose.orientation.w=data.rotation.w
                self.pub.publish(odom)




def main(args=None):
    rclpy.init(args=args)

    node = Talker()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
