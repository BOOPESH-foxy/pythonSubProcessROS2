import subprocess

def set_wifi_status(state):
    set_state = state
    nmcli_output = subprocess.run(['nmcli', 'radio', 'wifi', set_state],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    wifi_status = find_wifi_status()
    if(wifi_status == True):
        return True
    elif(wifi_status == False):
        return False

def find_wifi_status():
    nmcli_output = subprocess.run(['nmcli', 'radio', 'wifi'],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    wifi_status = nmcli_output.stdout.split()
    if(wifi_status[0] == 'enabled'):
        return True
    elif(wifi_status[0] == 'disabled'):
        return False
     

def get_wifi_list():
        wifi_ssid_list = []
        try:
            result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
            lines = result.stdout.split('\n')
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


def check_wifi_connection():    
        try:
            result = subprocess.check_output(['iwgetid', '--raw'])
            ssid = result.strip().decode('utf-8')
            if (ssid):
                return True
            else:
                return False
            
        except Exception as e:
            print(e)


def connect_wifi(ssid,password):
    ssid,password = ssid,password
    out = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    status = "Connected"
    return status


def disconnect_wifi(ssid):
    ssid = ssid
    out = subprocess.run(['nmcli', 'connection', 'down', ssid],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    status = "Disconnected"
    return status
