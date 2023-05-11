import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3


class TranslateQuaternion(Node):

    def __init__(self):
        super().__init__('translate_quaternion')
        self.subscription = self.create_subscription(
            Vector3,
            'RPYinfo',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"' % msg.data)
        Roll = msg.x
        Pitch = msg.y
        Yaw = msg.z
        print("Roll: " + Roll + ", ")
        print("Pitch: " + Pitch + ", ")
        print("Yaw: " + Yaw + "\n")


def main(args=None):
    rclpy.init(args=args)

    translate_quaternion = TranslateQuaternion()

    rclpy.spin(translate_quaternion)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    translate_quaternion.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()