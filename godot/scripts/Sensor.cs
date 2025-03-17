using Godot;
using System;

public partial class Sensor : Node3D
{
    private double _temperature = 20;

    [Export]
    public double Temperature
    {
        get => _temperature;
        set
        {
            if (_temperature != value) // Only update if the value is different
            {
                _temperature = value;
                Update();
            }
        }
    }

    private void Update()
    {
        UpdateLabel();
    }

    private void UpdateLabel()
    {
        Label3D label = GetNode<Label3D>("SensorLabel");
        label.Text = Temperature.ToString("F2") + "°C";
    }


    public override void _Ready()
    {
        Update();
    }
}
