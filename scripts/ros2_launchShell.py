import subprocess
import ros2_commands
import rclpy

class LifeCycleTriggerNodeClass():
    def __init__(self):
        self.commands = ros2_commands.commands
        self.isPresent = 0
        
    def rosTopicSubscriber(self):
        print(f'''subscribing to the topic {self.topic}''')
        pros = subprocess.Popen(
            f'''ros2 topic echo {self.topic}''',
            shell=True,
            executable="/usr/bin/zsh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Process created with ID: {}".format(pros.pid))
        for line in pros.stdout:
                print(line, end='')
    
    def popenProcess(self,commands):
        pros = subprocess.Popen(
            commands[0],
            shell=True,
            executable="/usr/bin/zsh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            self.topic = "/chatter"
            for line in pros.stdout:
                print(line, end='')
                if self.topic in (line):
                    self.isPresent = 1
                    break
            if(self.isPresent):
                self.rosTopicSubscriber()
            else:
                print("topic",self.topic,"not found!")
                    
                                    
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            pros.terminate()
            pros.wait()
            
        errors = pros.stderr.read()
        if errors:
            print(f"Errors: {errors}") 
    
    
if __name__ == "__main__":
    classObject = LifeCycleTriggerNodeClass()
    result = classObject.popenProcess(ros2_commands.commands)
    