import asyncio
import rclpy
from rclpy.node import Node
from iris_bluetooth.srv import ListBleDevices
from bleak import BleakScanner

class ListBleDevicesNode(Node):

    def __init__(self):
        super().__init__('ListBleDevicesNode')
        self.ble_service = self.create_service(ListBleDevices, 'iris/BleDevicesNode', self.bleDevice_listCallback_sync)

    async def bleDevice_listCallback(self, request, response):
        try:
            ble_devices = []
            list_devices = await BleakScanner.discover()
            for d in list_devices:
                ble_devices.append(d.address)
            print(ble_devices)
            response.blestate = "On"
            response.bledevices = ble_devices

        except Exception as e:
            if "No powered Bluetooth adapters found" in str(e):
                response.blestate = "Off"
                response.bledevices = []
            else:
                response.blestate = "Error"
                response.bledevices = []

        return response

    def bleDevice_listCallback_sync(self, request, response):
        asyncio.run(self.bleDevice_listCallback(request, response))
        return response

def main(args=None):
    rclpy.init(args=args)
    node = ListBleDevicesNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()