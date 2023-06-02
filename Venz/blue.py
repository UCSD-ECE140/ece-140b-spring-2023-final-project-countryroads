import asyncio
from bleak import BleakScanner, BleakClient

async def enable_notifications(client, service_uuid, characteristic_uuid):
    await client.start_notify(characteristic_uuid, notification_handler)

async def notification_handler(sender: int, data: bytearray):
    # Handle the received notification data
    print("Received notification data:", data.decode('ascii'))

async def read_characteristic_values(service_uuid, characteristic_uuid):
    scanner = BleakScanner()

    async with scanner as scanner:
        await scanner.start()
        await asyncio.sleep(5)  # Scan for 5 seconds

        device = "7D9589EC-E5CC-33BC-2B4A-460AB9DCAA5F"
        async with BleakClient(device) as client:
            try:
                await client.connect()

                # Enable notifications for the characteristic
                await enable_notifications(client, service_uuid, characteristic_uuid)

                # Keep the program running to receive notifications
                while True:
                    await asyncio.sleep(1)

            except Exception as e:
                print(f"Failed to read characteristic value for {device}: {str(e)}")
                await client.disconnect()
            finally:
                print("Disconnecting...")
                await client.stop_notify(characteristic_uuid)
                await client.disconnect()

async def main():
    service_uuid = "19B10000-E8F2-537E-4F6C-D104768A1214"  # Replace with your service UUID
    characteristic_uuid = "19B10001-E8F2-537E-4F6C-D104768A1214"  # Replace with your characteristic UUID

    await read_characteristic_values(service_uuid, characteristic_uuid)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

