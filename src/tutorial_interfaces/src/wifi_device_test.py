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

# wifi_ssids = list_wifi_ssids()
wifi_status = wifi_status()
