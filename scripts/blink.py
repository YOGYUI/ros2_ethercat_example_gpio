import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class BlinkPublisher(Node):
    def __init__(self):
        super().__init__("blink_publisher")
        self.value = 1
        self.publisher = self.create_publisher(Float64MultiArray, "/output_controller0/commands", 1)
        self.timer = self.create_timer(1.0, self.period_publish)

    def period_publish(self):
        msg = Float64MultiArray()
        msg.data = [float(self.value)]
        self.publisher.publish(msg)
        if self.value == 1:
            self.value = 0
        else:
            self.value = 1

def main(args=None):
    rclpy.init(args=args)
    node = BlinkPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
