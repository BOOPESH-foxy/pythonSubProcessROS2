import subprocess
from service_talker import ros2_commands
import rclpy
# from example_interfaces.srv import Trigger
from rclpy.node import Node
from std_srvs.srv import Trigger


class LifeCycleTriggerNodeClass(Node):
    def __init__(self):
        
        super().__init__('ServiceTriggerSubProcess')
        self.process = None
        self.srv_start = self.create_service(Trigger,'start_talker',self.StartTalker_CallBack)
        self.srv_stop = self.create_service(Trigger,'stop_talker',self.StopTalker_CallBack)
        self.commands = ros2_commands.SourceCommands
        
    def StartTalker_CallBack(self,request,response):
        if self.process is None:
            self.get_logger().info('entering the subprocess')
            self.process = subprocess.Popen(
                self.commands[0],
                shell=True,
                executable="/usr/bin/zsh",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )   
            response.success = True
            response.message = "started Talker !"
        else:
            response.success = False
            response.message = "Process have already started !"  

        return response 
            
    def StopTalker_CallBack(self,request,response):
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None
            response.success = True
            response.message = 'Process stopped !'
            
        else:
            response.success = False
            response.message = 'Process is not running !'
            
        return response
    
def main(args=None):
    rclpy.init()
    classObject = LifeCycleTriggerNodeClass()
    rclpy.spin(classObject)
    rclpy.shutdown()
        
if __name__ == "__main__":
    main()
    