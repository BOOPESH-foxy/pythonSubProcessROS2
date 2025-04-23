import asyncio
from bleak import BleakScanner

async def main():
    try:
        devices = await BleakScanner.discover()
        for d in devices:
            print("name:",d.name,d.address)

    except Exception as e:
        if "No powered Bluetooth adapters found" in str(e):
            print("Bluetooth state: off")
        else:
            print("error!")
asyncio.run(main())


# import asyncio
# from bleak import BleakClient

# address = "58:10:31:9F:E2:5E"

# async def main(address):
#     client = BleakClient(address)
    
#     try:
#         await client.connect()
#         if await client.is_connected():
#             print(f"Connected to {address}")
            
#             while True:
#                 await asyncio.sleep(1)  # Sleep for 1 second to keep the event loop running
#         else:
#             print(f"Failed to connect to {address}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         print(f"Program terminated. Connection to {address} will be closed.")

# asyncio.run(main(address))