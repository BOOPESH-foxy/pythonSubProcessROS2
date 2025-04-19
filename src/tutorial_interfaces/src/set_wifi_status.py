from tutorial_interfaces.srv import SetWifiStatus
import rclpy
from rclpy.node import Node
import subprocess


class SetWifiNode(Node):

    def __init__(self):
        super().__init__('SetWifiNode')
        self.service = self.create_service(SetWifiStatus,"iris/setWifiService",self.SetWifi_Callback)

    def SetWifi_Callback(self,request,response):
        if(request.connectwifi):
            connectionAccess_list = request.connectwifi
            ssid,password = connectionAccess_list[0],connectionAccess_list[1]
            out = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password],
                                    capture_output=True,
                                    text=True,
                                    check=True
                                    )
            response.status = "Connected"

        elif(request.disconnectwifi):
            ssid = request.disconnectwifi
            out = subprocess.run(['nmcli', 'connection', 'down', ssid],
                                    capture_output=True,
                                    text=True,
                                    check=True
                                    )
            response.status = "Disconnected"
            

        return response 

def main(args=None):
    rclpy.init(args=args)
    node = SetWifiNode()
    rclpy.spin(node)
    rclpy.shutdown(node)

if __name__ == "__main__":
    main()