import pika
import json
from influxdb_client import InfluxDBClient, Point, WriteOptions

# InfluxDB connection
influx_url = "http://localhost:8086"
influx_token = "yzSihCPVQFAWOKO0eYdPygLoX8vg8X8xkIh9iVI8ka5L6BA9buDT2FsA1XEv6ztYOLSNG9NkFjVWzfT0DNmuWQ=="  # Replace with your token
org = "Permafrost-organization"
bucket = "Permafrost-bucket"

client = InfluxDBClient(url=influx_url, token=influx_token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

rabbitmq_host = 'localhost'
exchange_name = 'PermafrostExchange'
routing_key = 'permafrost-routing-key'
queue_name = 'TemperatureQueue'

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"Received message: {message}")

    try:
        filename, temperature = message.split(": ")
        temperature = float(temperature)

        if temperature != -999:  # Skip invalid temperature readings
            # Create a new InfluxDB point
            point = Point("temperature") \
                .tag("sensor", filename) \
                .field("value", temperature)
            
            # Write the point to InfluxDB
            write_api.write(bucket=bucket, record=point)
            print(f"Stored to InfluxDB: {filename} - {temperature}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Set up RabbitMQ consumer
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=False)
channel.queue_declare(queue=queue_name, durable=False)
channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for messages...")
channel.start_consuming()
