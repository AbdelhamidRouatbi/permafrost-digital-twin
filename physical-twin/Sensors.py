
import os
import asyncio
import aio_pika
import json
import time
from pathlib import Path

async def send_temperature_data_to_rabbitmq(file_name):
    # RabbitMQ server details
    rabbitmq_host = 'localhost'
    exchange_name = 'PermafrostExchange'
    routing_key = 'permafrost-routing-key'
    queue_name = 'TemperatureQueue'

    # Setup RabbitMQ connection and channel using aio_pika
    connection = await aio_pika.connect_robust(f'amqp://{rabbitmq_host}')
    async with connection:
        channel = await connection.channel()  # Create a channel
        await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT, durable=False)
        queue = await channel.declare_queue(queue_name, durable=False)
        await queue.bind(exchange_name, routing_key=routing_key)

        # Get the file name without the .csv extension
        sensor_name = os.path.basename(file_name).replace(".csv", "")

        # Read the configuration file for frequency
        config_path = "config.json"
        with open(config_path, 'r') as file:
            config = json.load(file)
        frequency = config["frequency"]

        with open(file_name, 'r') as file:
            # Skip the header row
            next(file)

            timestep = 0  # initial timestamp in minutes

            # Loop through the csv file line by line asynchronously
            for line in file:
                line = line.strip()
                columns = line.split(",")
                sensor_data = float(columns[1])

                # Skip if the sensor value is -999 (missing value)
                if sensor_data == -999: continue

                # The message includes the file name and the sensor reading
                message = {
                    "sensor_name": sensor_name,
                    "temperature": sensor_data
                }
                print("sending")
                # Send the message to the RabbitMQ queue asynchronously
                await channel.default_exchange.publish(
                    aio_pika.Message(body=json.dumps(message).encode()),
                    routing_key=routing_key
                )
                print("sent")

                print(f"Sent: {message}")
                timestep += 30  # next readings happen after 30 minutes
                await asyncio.sleep(frequency)  # Asynchronous sleep

async def main():
    # Get list of all CSV files with relative paths in the 'data/' directory
    files = [f for f in os.listdir('data') if f.endswith('.csv') and os.path.isfile(os.path.join('data', f))]

    # Create a list of async tasks to run for each file
    tasks = []
    for file in files:
        file_path = os.path.join('data', file)
        tasks.append(send_temperature_data_to_rabbitmq(file_path))

    # Run all tasks asynchronously
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Pass the coroutine to asyncio.run
    asyncio.run(main())
