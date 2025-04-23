from iris_bluetooth.srv import SetBle
import rclpy
from rclpy.node import Node
from bleak import BleakClient
import asyncio

class SetBluetoothNode(Node):

    def __init__(self):
        super().__init__("ConnectBluetoothNode")
        self.create_service(SetBle,"iris/connect_bluetooth",self.connect_BluetoothCallback)
        # self.create_service(SetBle,"iris/disconnect_bluetooth",self.disconnect_BluetoothCallback)

    async def connect_BluetoothCallback(self,request,response):
        try:
            client = BleakClient(request.deviceaddress)
            await client.connect()
            response.status = "Connected"
            if await client.is_connected():
                self.status = 1
                while(self.status):
                    await asyncio.sleep(1)
            
            else:
                print(f"Failed to connect to {request.deviceaddress}")
                response.statue = "connection failed !"

        except Exception as e:
            print(f"An error occurred: {e}")
            response.status = "error"
        finally:
            print(f"Program terminated. Connection to {request.deviceaddress} will be closed.")
            
        return response


def main(args=None):
    rclpy.init(args=args)
    node = SetBluetoothNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()