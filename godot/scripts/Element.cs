using Godot;
using System;
using System.Collections.Generic;

public partial class Element : Node3D
{
	[Export] double Temperature { get; set; } = 20;

	public void interpolate(List<Sensor> sensors)
	{
		double numerator = 0;
		double denominator = 0;

		foreach (Sensor sensor in sensors)
		{
			float invDistance = 1 / (MathF.Sqrt(
							(this.Position.X - sensor.Position.X) * (this.Position.X - sensor.Position.X) +
							(this.Position.Z - sensor.Position.Z) * (this.Position.Z - sensor.Position.Z))
				);
			numerator += invDistance * sensor.Temperature;
			denominator += invDistance;
		}

		double result = numerator / denominator;
		Temperature = result;
		updateColor();
	}

	private void updateColor()
	{
		float minT = 0f; // Minimum temperature (blue)
		float maxT = 100f;  // Maximum temperature (red)
		if (GetNode<MeshInstance3D>("ElementMesh") is MeshInstance3D meshInstance)
		{
			var mat = meshInstance.GetSurfaceOverrideMaterial(0) as StandardMaterial3D;
			if (mat == null)
			{
				mat = new StandardMaterial3D();
			}
			float ratio = ((float)Temperature - minT) / (maxT - minT);
			mat.AlbedoColor = new Color(ratio, ratio / 2, 1 - ratio, 1f);
			meshInstance.SetSurfaceOverrideMaterial(0, mat);
			//meshInstance.Transparency = 0.8f;
		}
	}

}
