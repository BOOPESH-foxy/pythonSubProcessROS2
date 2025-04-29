import wifi_control 
from iris_interfaces.srv import GetWifiStatus,WifiDiscovery,ConnectWifi,DisconnectWifi
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time 

class LinuxControlNode(Node):
    
    def __init__(self):
        super().__init__("LinuxControlNode")

        #services
        self.wifi_status_service = self.create_service(GetWifiStatus,'iris1/WiFi/Status',self.wifi_status_callback)
        self.wifi_devices_discovery_service = self.create_service(WifiDiscovery,'iris1/WiFi/Devices',self.wifi_devices_callback)
        self.set_wifi_service = self.create_service(ConnectWifi,'iris1/WiFi/ConnectWiFi',self.connect_wifi_callback)
        self.disconnect_wifi_service = self.create_service(DisconnectWifi,'iris1/WiFi/DisconnecWiFi',self.disconnect_wifi_callback)
        #publishers
        self.device_list_publisher = self.create_publisher(String,'iris1/WiFi/DevicesPublisher',1)
        
    
    def wifi_devices_publisher_callback(self):
        msg = String()
        msg.data = str(wifi_control.get_wifi_list())
        self.device_list_publisher.publish(msg)


    def wifi_status_callback(self,request,response):
        self.get_logger().info('Status: FIND, ON, OFF')

        if(request.service == 'FIND'):
            wifi_status = wifi_control.find_wifi_status()
            if(wifi_status):
                response.status = "Enabled"
                return response
            else:
                response.status = "Disabled"
                return response
            
        elif(request.service == 'ON'):
            self.get_logger().info(request.service)
            wifi_status = wifi_control.set_wifi_status('on')
            if(wifi_status == True):
                response.status = "Enabled"
                return response

        elif(request.service == 'OFF'):
            wifi_status = wifi_control.set_wifi_status('off')
            if(wifi_status == False):
                response.status = "Disabled"
                return response


    def wifi_devices_callback(self,request,response):

        timestamp = int(time.time())
        response.timestamp = timestamp

        if(request.wifidiscovery == "ON"):
            self.device_list = wifi_control.get_wifi_list()
            response.discoverystatus = "Enabled"
            time_period = 2
            self.timer = self.create_timer(time_period,self.wifi_devices_publisher_callback)
            
        elif(request.wifidiscovery == "OFF"):
            self.device_list_publisher.destroy()
            response.discoverystatus = "Disabled"

        return response
    

    def connect_wifi_callback(self,request,response):
        ssid,password = request.ssid,request.password
        set_wifi_status = wifi_control.connect_wifi(ssid,password)
        if(set_wifi_status == "Connected"):
            response.status = "Connected"
        
        return response

    
    def disconnect_wifi_callback(self,request,response):
        ssid = request.ssid
        disconnect_wifi_status = wifi_control.disconnect_wifi(ssid)
        if(disconnect_wifi_status == "Disconnected"):
            response.status = "Disconnected"
        
        return response

def main(args=None):
    rclpy.init()
    node = LinuxControlNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()