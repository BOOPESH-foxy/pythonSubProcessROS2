import subprocess
import Jetson.GPIO as GPIO
import time
import signal
import sys

class GetWifiStatus:

    def __init__(self):
        self.gpio_channels = [15, 29]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_channels, GPIO.OUT, initial=GPIO.LOW)

    def wifiStatus_call(self):
        try:
            iwget_output = subprocess.run(['iwgetid', '--raw'],
                                 capture_output=True,
                                 text=True,
                                 check=True)
            wifi_status = iwget_output.stdout

            if (wifi_status):
                GPIO.output(self.gpio_channels[0], GPIO.HIGH)
                GPIO.output(self.gpio_channels[1], GPIO.LOW)
            else:
                GPIO.output(self.gpio_channels[1], GPIO.HIGH)
                GPIO.output(self.gpio_channels[0], GPIO.LOW)
        
        except subprocess.CalledProcessError:
            GPIO.output(self.gpio_channels[1], GPIO.HIGH)
            GPIO.output(self.gpio_channels[0], GPIO.LOW)

    def cleanup(self):
        print("on shutdown - to led:red")
        GPIO.output(self.gpio_channels[1], GPIO.HIGH)
        GPIO.output(self.gpio_channels[0], GPIO.LOW)
        # GPIO.cleanup(self.gpio_channels)

def main():
    obj = GetWifiStatus()

    def signal_handler(sig, frame):
        obj.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler) 
    try:
        while True:
            obj.wifiStatus_call()
            time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        obj.cleanup()

if __name__ == "__main__":
    main()