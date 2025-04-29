import subprocess

def set_bluetooth_status(state):
    set_state = state
    nmcli_output = subprocess.run(['bluetoothctl', 'power',  set_state],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    bluetooth_status = find_bluetooth_status()
    if(bluetooth_status == True):
        return True
    elif(bluetooth_status == False):
        return False

def find_bluetooth_status():
    nmcli_output = subprocess.run(['bluetoothctl', 'show', '| grep', 'Powered: yes'],
                            capture_output=True,
                            text=True,
                            check=True
                            )
    bluetooth_status = nmcli_output.stdout.split()
    if(bluetooth_status[0]):
        return True
    else:
        return False
    
def list_bluetooth_devices():
    pass

def connect_bluetooth_device():
    pass

def disconnect_bluetooth_device():
    pass

