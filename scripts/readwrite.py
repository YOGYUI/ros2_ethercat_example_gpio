import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from control_msgs.msg import DynamicJointState, InterfaceValue

class ReadWriteNode(Node):
    def __init__(self):
        super().__init__("gpio_read_write_node")
        self.input_byte0: int = 0
        self.input_byte1: int = 0
        self.output_byte0: int = 0
        self.output_byte1: int = 0

        self.subscriber = self.create_subscription(
            DynamicJointState, "/dynamic_joint_states", self.callback_dynamic_joint_states, 10)
        self.publisher0 = self.create_publisher(
            Float64MultiArray, "/output_controller0/commands", 1)
        self.publisher1 = self.create_publisher(
            Float64MultiArray, "/output_controller1/commands", 1)

    def callback_dynamic_joint_states(self, msg: DynamicJointState):
        interface_value: InterfaceValue = msg.interface_values[0]
        names = interface_value.interface_names
        values = interface_value.values
        idx0 = names.index("dig.in.byte0")
        self.input_byte0 = int(values[idx0])
        idx1 = names.index("dig.in.byte1")
        self.input_byte1 = int(values[idx1])
        self.handle_input()
        
    def publish_output_byte0(self, value: int):
        msg = Float64MultiArray()
        self.output_byte0 = max(0, min(0xFF, value))
        msg.data = [float(self.output_byte0)]
        self.publisher0.publish(msg)

    def publish_output_byte1(self, value: int):
        msg = Float64MultiArray()
        self.output_byte1 = max(0, min(0xFF, value))
        msg.data = [float(self.output_byte1)]
        self.publisher0.publish(msg)

    def handle_input(self):
        # test code (bypass input to output)
        print(self.input_byte0, self.input_byte1)
        self.publish_output_byte0(self.input_byte0)
        self.publish_output_byte1(self.input_byte1)


def main(args=None):
    rclpy.init(args=args)
    node = ReadWriteNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
