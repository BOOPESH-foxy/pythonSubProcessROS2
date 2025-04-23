import subprocess
import Jetson.GPIO as GPIO
import time
import signal
import sys
import os

class GetWifiStatus:

    def __init__(self):
        self.channels = [15, 29]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channels, GPIO.OUT, initial=GPIO.LOW)

    def wifiStatus_call(self):
        try:
            out = subprocess.run(['nmcli', 'connection', 'show', '--active'],
                                 capture_output=True,
                                 text=True,
                                 check=True)
            status = out.stdout
            wifi_status = status.find("wifi")

            if wifi_status > 0:
                GPIO.output(self.channels[0], GPIO.HIGH)
                GPIO.output(self.channels[1], GPIO.LOW)
                print("wifi - up")
            elif wifi_status == -1:
                GPIO.output(self.channels[1], GPIO.HIGH)
                GPIO.output(self.channels[0], GPIO.LOW)
                print("wifi - down")
        
        except subprocess.CalledProcessError as e:
            print(f"Error running nmcli: {e}")
            GPIO.output(self.channels[1], GPIO.HIGH)
            GPIO.output(self.channels[0], GPIO.LOW)

    def cleanup(self):
        print("on shutdown - to led:red")
        GPIO.output(self.channels[1], GPIO.HIGH)
        GPIO.output(self.channels[0], GPIO.LOW)
        GPIO.cleanup(self.channels)

def main():
    obj = GetWifiStatus()

    def signal_handler(sig, frame):
        obj.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler) 
    try:
        print(f"PID of the current process: {os.getpid()}")
        while True:
            obj.wifiStatus_call()
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        obj.cleanup()

if __name__ == "__main__":
    main()