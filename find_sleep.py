import asyncio
from bleak import BleakScanner, BleakClient

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
        # Process the sleep data here
        # For now, we'll just print the raw value
        return value
    except Exception as e:
        print(f"Failed to read from {char_uuid}: {e}")

async def connect_and_read_sleep_data(device):
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
        sleep_data_char_uuid = "00002a19-0000-1000-8000-00805f9b34fb"  # Example UUID from your screenshot
        if sleep_data_char_uuid in [char.uuid for service in services for char in service.characteristics if 'read' in char.properties]:
            print(f"Reading from characteristic {sleep_data_char_uuid}")
            sleep_data = await read_characteristic(client, sleep_data_char_uuid)
            print(f"Sleep data: {sleep_data}")
        await client.disconnect()
        print(f"Disconnected from {device.name}")
    except Exception as e:
        print(f"Failed to connect: {e}")

async def main():
    target_name = "Amazfit Band 7"  # Replace with your smartwatch's Bluetooth name
    device = await find_device(target_name)

    if device:
        print(f"Found device {target_name} with address {device.address}")
        await connect_and_read_sleep_data(device)
    else:
        print(f"Could not find device {target_name}")

if __name__ == "__main__":
    asyncio.run(main())

