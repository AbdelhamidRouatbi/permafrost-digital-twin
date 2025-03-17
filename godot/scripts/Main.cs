using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;


public partial class Main : Node
{
	[Export] public PackedScene ElementScene { get; set; }
	private List<Borehole> Boreholes = new List<Borehole>();
	private List<Sensor> Sensors = new List<Sensor>();
	private List<Element> Elements = new List<Element>();
	private HashSet<Vector3> OccupiedSpace = new HashSet<Vector3>();


	public override void _Ready()
	{
		setup();
		GD.Print("There are " + Boreholes.Count + " boreholes.");
		generateBoreholes();
		generateElements();
		updateElements();
	}

	private void generateBoreholes()
	{
		List<Sensor> generatedSensors;
		var r = new Random();
		foreach (Borehole borehole in Boreholes)
		{
			double t = r.NextDouble() * 100;
			generatedSensors = borehole.GetSensors();
			foreach (Sensor sensor in generatedSensors)
			{
				sensor.Temperature = t;
				AddChild(sensor);
				Sensors.Add(sensor);
				OccupiedSpace.Add(sensor.Position);
			}
			generatedSensors.Clear();
		}
	}

	private void generateElements()
	{
		float minX = Sensors.Min(s => s.Position.X);
		float maxX = Sensors.Max(s => s.Position.X);
		float minZ = Sensors.Min(s => s.Position.Z);
		float maxZ = Sensors.Max(s => s.Position.Z);
		float maxDepth = 50;
		GD.Print("computing..");

		for (float x = minX; x <= maxX; x++)
		{
			for (float y = 0; y >= -maxDepth; y--)
			{
				for (float z = minZ; z <= maxZ; z++)
				{
					Vector3 pos = new Vector3(x, y, z);
					if (!(OccupiedSpace.Contains(pos) || Sensors.Any(s => s.Position.X == x && s.Position.Z == z)))
					{
						Element element = (Element)ElementScene.Instantiate();
						element.Position = pos;
						AddChild(element);
						Elements.Add(element);
					}
				}
			}
		}
		GD.Print("done");
		GD.Print(Elements.Count);
	}

	private void setup()
	{
		foreach (Node child in GetChildren())
		{
			if (child is Borehole typedChild)
			{
				Boreholes.Add(typedChild);
			}
		}
	}

	private void updateElements()
	{
		foreach (Element e in Elements)
		{
			e.interpolate(Sensors);
		}
	}

	private Random randomizer = new Random();

	public void _do()
	{
		foreach (var s in Sensors)
		{
			s.Temperature = randomizer.NextDouble() * 100;
		}
		updateElements();
	}
}
