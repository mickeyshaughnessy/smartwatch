import asyncio
import time
from bleak import BleakScanner, BleakClient

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Time remaining: {timeformat}", end='\r')
        time.sleep(1)
        seconds -= 1
    print("Time remaining: 00:00")

async def scan_devices(duration=30):
    print(f"Scanning for devices for {duration} seconds...")
    devices = await BleakScanner.discover(timeout=duration)
    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")
    return devices

async def find_device(target_name, retries=10, delay=10):
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} to find {target_name}")
        devices = await scan_devices(duration=20)
        for device in devices:
            if device.name and target_name in device.name:
                return device
        print(f"Device not found, waiting {delay} seconds before retrying...")
        await asyncio.sleep(delay)
    return None

async def read_characteristic(client, char_uuid):
    try:
        value = await client.read_gatt_char(char_uuid)
        print(f"Read from {char_uuid}: {value}")
    except Exception as e:
        print(f"Failed to read from {char_uuid}: {e}")

async def connect_to_device(device):
    try:
        client = BleakClient(device, timeout=30.0)
        await client.connect()
        print(f"Connected to {device.name}")
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}, Properties: {char.properties}")

        # Choose a characteristic that supports reading
        read_char_uuid = "00002a19-0000-1000-8000-00805f9b34fb"  # Example UUID from your screenshot
        if read_char_uuid in [char.uuid for service in services for char in service.characteristics if 'read' in char.properties]:
            print(f"Reading from characteristic {read_char_uuid}")
            await read_characteristic(client, read_char_uuid)
        await client.disconnect()
        print(f"Disconnected from {device.name}")
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main():
    target_name = "Amazfit Bip 3"  # Replace with your smartwatch's Bluetooth name
    device = await find_device(target_name)

    if device:
        print(f"Found device {target_name} with address {device.address}")
        await connect_to_device(device)
    else:
        print(f"Could not find device {target_name}")

if __name__ == "__main__":
    asyncio.run(main())

