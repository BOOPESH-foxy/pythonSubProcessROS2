import subprocess
import rclpy
from rclpy.node import Node
from tutorial_interfaces.srv import ListWifiDevices
import time
import wifi

class DeviceListNode(Node):
    def __init__(self):
        super().__init__('device_list_node')
        self.srv = self.create_service(ListWifiDevices, 'list_wifi_devices', self.list_wifi_devices_callback)

    def list_wifi_devices_callback(self, request, response):
        current_time = int(time.time())
        response.timestamp = current_time

        is_connected = self.check_wifi_connection()
        if(is_connected):
            response.isconnected = True
        else:
            response.isconnected = False

        devices_list = self.get_wifi_list()
        response.devices = devices_list
        return response

    def get_wifi_list(self):

        wifi_list = []
        try:
            result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
            lines = result.stdout.split('\n')
            ssid = []
            for line in lines:
                if not line:
                    continue
                wifi_data = line.split()
                ssid.append(wifi_data[2])
    
        except Exception as e:
            wifi_list.append("wifi state: off")    
        return wifi_list


    def check_wifi_connection(self):
            
        try:
            result = subprocess.check_output(['iwgetid', '--raw'])
            ssid = result.strip().decode('utf-8')
            
            if (ssid):
                return True
            else:
                return False
        except Exception as e:
            print(e)

def main(args=None):
    rclpy.init(args=args)
    node = DeviceListNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()