using Godot;
using System.Collections.Generic;

public partial class Borehole : Node3D
{
	[Export] public int Depth { get; set; } = 10;
	[Export] public int SensorCount { get; set; } = 5;
	[Export] public PackedScene SensorScene { get; set; }

	public List<Sensor> GetSensors()
	{
		List<Sensor> sensors = new List<Sensor>();
		double x = this.Position.X;
		double z = this.Position.Z;
		double step = Depth / SensorCount;
		for (int i = 0; i <= SensorCount; i++)
		{
			Sensor sensor = (Sensor)SensorScene.Instantiate();
			double y = i * step;
			sensor.Position = new Vector3((float)x, -(float)y, (float)z);
			sensors.Add(sensor);
		}
		return sensors;
	}

}
