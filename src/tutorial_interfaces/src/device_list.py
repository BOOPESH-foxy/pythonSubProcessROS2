import subprocess
import rclpy
from rclpy.node import Node
from tutorial_interfaces.srv import ListWifiDevices
import time
from std_msgs.msg import String
import wifi

class DeviceListNode(Node):

    def __init__(self):

        super().__init__('DeviceList')
        self.list_wifi_service = self.create_service(ListWifiDevices, 'start_wifi_discovery', self.start_wifi_discovery_callback)
        self.stop_wifi_discovery = self.create_service(ListWifiDevices,'stop_wifi_descovery',self.stop_wifi_discovery_callback)
        
        self.list_wifi_publisher = self.create_publisher(String,'iris_wifi_devices',1)
        time_period = 2
        self.timer = self.create_timer(time_period,self.wifi_list_callback)



    def wifi_list_callback(self):

        msg = String()
        msg.data = str(self.get_wifi_list())
        self.list_wifi_publisher.publish(msg)



    def start_wifi_discovery_callback(self, request, response):
        response.timestamp = int(time.time())
        response.discoverystatus = 'On'
        is_connected = self.check_wifi_connection()
        if(is_connected):
            response.isconnected = True

        else:
            response.isconnected = False

        devices_list = self.get_wifi_list()
        response.devices = devices_list

        return response



    def stop_wifi_discovery_callback(self,request,response):
        
        response.timestamp = int(time.time())
        is_connected = self.check_wifi_connection()
        if(is_connected):
            response.isconnected = True

        else:
            response.isconnected = False
        response.discoverystatus = 'Off'
                
        return response
    

    def get_wifi_list(self):

        wifi_ssid_list = []
        try:
            self.result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
            lines = self.result.stdout.split('\n')
            index = 2
            for line in lines[1:]:
                if not line:
                    continue
                wifi_data = line.split()
                wifi_ssid_list.append(wifi_data[index])
                index = 1
    
        except Exception as e:
            wifi_ssid_list.append("wifi state: off")    
        return wifi_ssid_list



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