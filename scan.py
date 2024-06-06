import asyncio
from bleak import BleakScanner

async def scan_devices():
    devices = await BleakScanner.discover()
    return devices

async def main():
    devices = await scan_devices()
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(main())
