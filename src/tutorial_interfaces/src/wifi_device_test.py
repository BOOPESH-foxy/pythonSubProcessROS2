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

wifi_ssids = list_wifi_ssids()
