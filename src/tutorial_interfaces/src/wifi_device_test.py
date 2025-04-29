import subprocess

def list_wifi_ssids():
    try:
        result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        ssids = []
        index = 2
        for line in lines[1:]:
            if not line:
                continue
            data = line.split()
            ssids.append(data[index])
            index = 1
        print(ssids)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []
    
def wifi_status():
    try:
        status = subprocess.run(['nmcli','radio', 'wifi'],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        result = status.stdout.split()
        if(result[0] == 'enabled'):
            print('wifi status: On')
        else:
            print("wifi status: Off")
        print(result)
        
    except Exception as e:
        print(e)

def set_wifi():
        string_list = []
        string_list = ['RapplWifi','rappl4567']
        ssid,password = string_list[0],string_list[1]
        out = subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        print(out)

def disconnect_wifi():
    wifi = 'boo 1'
    print(wifi)
    out = subprocess.run(['nmcli', 'connection', 'down', wifi],
                                    capture_output=True,
                                    text=True,
                                    check=True
                                    )
# wifi_ssids = list_wifi_ssids()
# wifi_status = wifi_status()
set_wifi = set_wifi()
# disconnect_wifi = disconnect_wifi()