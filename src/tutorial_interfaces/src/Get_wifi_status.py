import subprocess
import rclpy
from tutorial_interfaces.srv import GetWifiStatus
from rclpy.node import Node
import Jetson.GPIO as GPIO

class GetWifiStatusNode(Node):

    def __init__(self):
        super().__init__("GetWifiStatus")
        self.service = self.create_service(GetWifiStatus,"iris/Get_wifi_status",self.wifiStatus_callback)
        self.channels = [15,29]
    def wifiStatus_callback(self,request,response):
        out = subprocess.run(['nmcli', 'radio', 'wifi'],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        status = out.stdout.split()
        if(status[0] == 'enabled'):
            response.status=True
            GPIO.output(self.channels[0],GPIO.HIGH)
        else:
            response.status=False
            GPIO.output(self.channels[1],GPIO.HIGH)

        return response

def main(args=None):
    rclpy.init(args=args)
    node = GetWifiStatusNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()