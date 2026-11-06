import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped


class WaypointNavigator(Node):

    def __init__(self):
        super().__init__('waypoint_navigator')

        self.client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.waypoints = [
            (0.341, 0.009, 0.0),
            (1.591, 1.009, 0.0),
            (3.591, 1.009, 0.0),
        ]

        self.current_waypoint = 0

        self.get_logger().info('Waypoint Navigator Started')

        self.client.wait_for_server()

        self.send_next_goal()

    def send_next_goal(self):

        if self.current_waypoint >= len(self.waypoints):
            self.get_logger().info(
                'All waypoints completed!'
            )
            rclpy.shutdown()
            return

        x, y, yaw = self.waypoints[self.current_waypoint]

        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()

        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y

        import math

        goal.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal.pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.get_logger().info(
            f'Sending waypoint {self.current_waypoint + 1}: '
            f'x={x}, y={y}'
        )

        self.client.send_goal_async(
            goal
        ).add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected!')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted!')

        goal_handle.get_result_async().add_done_callback(
            self.result_callback
        )

    def result_callback(self, future):

        result = future.result()

        if result.status == 4:
            self.get_logger().info(
                f'Waypoint {self.current_waypoint + 1} reached!'
            )

            self.current_waypoint += 1
            self.send_next_goal()

        else:
            self.get_logger().error(
                f'Navigation failed. Status: {result.status}'
            )
            rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    node = WaypointNavigator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
