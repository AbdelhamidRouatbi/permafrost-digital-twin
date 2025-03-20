extends Node

var boreholes: Array = []
var sensors: Array = []
@onready var heatMap = $HeatMap

#var elements: Array = []
#var occupied_space: Dictionary = {}

func _ready():
	setup()
	print("There are " + str(boreholes.size()) + " boreholes.")
	generate_boreholes()
	generate_heatMap()
	
func generate_boreholes():
	for borehole in boreholes:
		var generated_sensors = borehole.get_sensors()
		for sensor in generated_sensors:
			sensor = sensor as Sensor
			(sensor as Sensor).temperature = 20.0
			add_child(sensor)
			sensors.append(sensor)
		generated_sensors.clear()
		
func generate_heatMap():
	var min_x = sensors.map(func(s): return s.position.x).min()
	var max_x = sensors.map(func(s): return s.position.x).max()
	var min_z = sensors.map(func(s): return s.position.z).min()
	var max_z = sensors.map(func(s): return s.position.z).max()
	var max_y = 1.0
	var min_y = -10.0
	
	var box_size = Vector3(max_x - min_x, max_y - min_y, max_z - min_z)
	var center_position = Vector3((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
	heatMap.scale = box_size
	heatMap.transform.origin = center_position
	
func setup():
	for child in get_children():
		if child is Borehole:
			boreholes.append(child)
			
func _process(delta):
	var data = PackedFloat32Array()
	for sensor in sensors:
		var position = sensor.position
		var temperature = sensor.temperature
		data.append(position.x)
		data.append(position.y)
		data.append(position.z)
		data.append(temperature)
		
	if heatMap.get_active_material(0):
		heatMap.get_active_material(0).set_shader_parameter("sensors", data)
		heatMap.get_active_material(0).set_shader_parameter("sensor_count", sensors.size())
		

func _on_timer_timeout() -> void:
	for sensor in sensors:
		sensor.temperature = randf_range(0.0, 100.0)
