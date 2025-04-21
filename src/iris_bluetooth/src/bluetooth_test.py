import asyncio
from bleak import BleakScanner

async def main():
    try:
        devices = await BleakScanner.discover()
        for d in devices:
            print("name:",d.name)

    except Exception as e:
        if "No powered Bluetooth adapters found" in str(e):
            print("Bluetooth state: off")
        else:
            print("error!")
asyncio.run(main())