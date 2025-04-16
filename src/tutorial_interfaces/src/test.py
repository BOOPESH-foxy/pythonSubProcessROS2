
import subprocess

def check_wifi_connection():
            
            result = subprocess.check_output(['iwgetid', '--raw'])
            ssid = result.strip().decode('utf-8')
            print(ssid)
            if result:
                return True
            else:

                return False
result = check_wifi_connection()
print(result)