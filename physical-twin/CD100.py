# setup
import os
import json
import pika
import time


# RabbitMQ server details
rabbitmq_host = 'localhost'
exchange_name = 'PermafrostExchange'
routing_key = 'permafrost-routing-key'
queue_name = 'TemperatureQueue'

# Setup RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Declare exchange and queue (similar to C#)
channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=False)
channel.queue_declare(queue=queue_name, durable=False)
channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

script_name = os.path.basename(__file__)  # Get script filename
name_without_ext, _ = os.path.splitext(script_name)  # Remove old extension
file_path = "data/" + name_without_ext + ".csv"  # Add new extension


config_path = "config.json"
with open(config_path, 'r') as file:
    config = json.load(file)
print(config["frequency"])
frequency = config["frequency"]

print(file_path)
with open(file_path, 'r') as file:
    # Skip the header row
    next(file)
    
    timestep = 0  # initial timestamp in minutes
    
    # Loop through the csv file line by line
    for line in file:
        line = line.strip()
        columns = line.split(",")
        sensor_data = ', '.join(columns)
        
        # The message includes the file name and the sensor reading
        message = f"{name_without_ext}: {columns[1]}"
        
        # Skip if the sensor value is -999
        if float(columns[1]) == -999: continue
        
        # Send the message to the RabbitMQ queue
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )
        
        print(f"Sent: {message}")
        timestep += 30  # next readings happen after 30 minutes
        time.sleep(frequency)
