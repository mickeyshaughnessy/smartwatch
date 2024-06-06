import asyncio
from bleak import BleakScanner, BleakClient

async def scan_devices(duration=30):
    print(f"Scanning for devices for {duration} seconds...")
    devices = await BleakScanner.discover(timeout=duration)
    return devices

async def read_battery_level(client):
    battery_level_uuid = "00002a19-0000-1000-8000-00805f9b34fb"
    try:
        value = await client.read_gatt_char(battery_level_uuid)
        battery_level = int.from_bytes(value, byteorder='little')
        print(f"Battery level: {battery_level}%")
        return battery_level
    except Exception as e:
        print(f"Failed to read battery level: {e}")

async def connect_and_read_battery_level(device):
    try:
        client = BleakClient(device, timeout=30.0)
        await client.connect()
        print(f"Connected to {device.name} with address {device.address}")
        await read_battery_level(client)
        await client.disconnect()
        print(f"Disconnected from {device.name}")
    except Exception as e:
        print(f"Failed to connect to {device.name} with address {device.address}: {e}")

async def main():
    target_name = "Amazfit Bip 3"  # Replace with your smartwatch's Bluetooth name
    devices = await scan_devices(duration=30)

    bip3_devices = [device for device in devices if target_name in (device.name or "")]
    
    if bip3_devices:
        for device in bip3_devices:
            await connect_and_read_battery_level(device)
    else:
        print(f"No devices named {target_name} found.")

if __name__ == "__main__":
    asyncio.run(main())

