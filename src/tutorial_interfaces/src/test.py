import subprocess

def list_wifi_ssids():
    try:
        result = subprocess.run(['nmcli', 'device', 'wifi', 'list'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        ssids = []
        for line in lines[1:]:
            if not line:
                continue
            data = line.split()
            ssids.append(data[2])
        print(ssids)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []

wifi_ssids = list_wifi_ssids()
