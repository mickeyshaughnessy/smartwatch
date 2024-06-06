import asyncio
from bleak import BleakScanner, BleakClient

async def scan_devices(duration=10):
    devices = await BleakScanner.discover(duration=duration)
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")
    return devices

async def find_device(target_name, retries=3, delay=5):
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} to find {target_name}")
        devices = await scan_devices(duration=10)
        for device in devices:
            if device.name and target_name in device.name:
                return device
        print(f"Device not found, waiting {delay} seconds before retrying...")
        await asyncio.sleep(delay)
    return None

async def connect_to_device(device):
    try:
        async with BleakClient(device) as client:
            print(f"Connected to {device.name}")
            services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"  Characteristic: {char.uuid}, Properties: {char.properties}")
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main():
    target_name = "Amazfit Band 7"  # Replace with your smartwatch's Bluetooth name
    device = await find_device(target_name)

    if device:
        print(f"Found device {target_name} with address {device.address}")
        await connect_to_device(device)
    else:
        print(f"Could not find device {target_name}")

if __name__ == "__main__":
    asyncio.run(main())

