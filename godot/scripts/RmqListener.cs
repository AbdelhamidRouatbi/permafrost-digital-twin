using Godot;
using System.Linq;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;

public partial class RmqListener : Node
{

	public override void _Ready()
	{
		//publish();
		listen();
	}


	private void publish()
	{
		GD.Print("sending message");

		ConnectionFactory factory = new();
		factory.Uri = new Uri("amqp://guest:guest@localhost:5672");
		factory.ClientProvidedName = "Rabbit Sender App";

		IConnection cnn = factory.CreateConnection();
		IModel channel = cnn.CreateModel();

		string exchangeName = "DemoExchange";
		string routingKey = "demo-routing-key";
		string queueName = "DemoQueue";

		channel.ExchangeDeclare(exchangeName, ExchangeType.Direct);
		channel.QueueDeclare(queueName, false, false, false, null);
		channel.QueueBind(queueName, exchangeName, routingKey, null);

		byte[] messageBodyBytes = Encoding.UTF8.GetBytes("Hello me");
		channel.BasicPublish(exchangeName, routingKey, null, messageBodyBytes);


		channel.Close();
		cnn.Close();

		GD.Print("Message sent!");
	}

	private void listen()
	{
		GD.Print("listening");

		ConnectionFactory factory = new();
		factory.Uri = new Uri("amqp://guest:guest@localhost:5672");
		factory.ClientProvidedName = "Rabbit Receiver App";

		IConnection cnn = factory.CreateConnection();
		IModel channel = cnn.CreateModel();

		string exchangeName = "PermafrostExchange";
		string routingKey = "permafrost-routing-key";
		string queueName = "TemperatureQueue";

		channel.ExchangeDeclare(exchangeName, ExchangeType.Direct);
		channel.QueueDeclare(queueName, false, false, false, null);
		channel.QueueBind(queueName, exchangeName, routingKey, null);
		channel.BasicQos(0, 1, false);

		var consumer = new EventingBasicConsumer(channel);
		consumer.Received += (sender, args) =>
		{
			var body = args.Body.ToArray();

			string message = Encoding.UTF8.GetString(body);


			processMessage(message);
			channel.BasicAck(args.DeliveryTag, false);
		};

		string consumerTag = channel.BasicConsume(queueName, false, consumer);
	}

	private void processMessage(string message)
	{
		var main = GetParent();
		if (main != null)
		{
			string[] parts = message.Split(": ");
			if (parts.Length != 2)
			{
				GD.PrintErr("Invalid message format: " + message);
			}
			else
			{
				string sensorName = parts[0].Trim();
				float temperature = parts[1].Trim().ToFloat() - 273;
				main.Call("processRmq", sensorName, temperature);
			}
		}
		else
		{
			GD.Print("no main found");
		}
	}
}
