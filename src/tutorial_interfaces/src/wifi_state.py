import subprocess
import Jetson.GPIO as GPIO

class GetWifiStatus():

    def __init__(self):
        self.channels = [15,29]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channels,GPIO.OUT,initial=GPIO.LOW)

    def wifiStatus_call(self):
        out = subprocess.run(['nmcli', 'radio', 'wifi'],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        status = out.stdout.split()
        if(status[0] == 'enabled'):
            GPIO.output(self.channels[0],GPIO.HIGH)
            print("PIN 15 HIGH")
        else:
            GPIO.output(self.channels[1],GPIO.HIGH)
            print("PIN 29 HIGH")

def main():
    obj = GetWifiStatus()
    obj.wifiStatus_call()

if __name__ == "__main__":
    main()