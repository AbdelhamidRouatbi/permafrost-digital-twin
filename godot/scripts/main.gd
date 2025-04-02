extends Node

var boreholes: Array = []
var sensors: Array = []
var sensorsBelow: Array = []
@onready var heatMap = $HeatMap
var heatmapInitialScale = Vector3()
#var elements: Array = []
#var occupied_space: Dictionary = {}

func _ready():
	generate_boreholes()
	generate_heatMap()
	print("There are " + str(sensors.size()) + " sensors.")
	
func generate_boreholes():
	var nodes = get_children()
	for node in nodes:
		if node is Sensor:
			sensors.append(node)
	for sensor in sensors:
		for i in range(1, 7):
			var s = sensor.duplicate()
			s.position = Vector3(s.position.x, -5.0*i, s.position.z)
			s.pos = s.position
			sensor.sensorsBelow.append(s)
			add_child(s)
			s.temperature = sensor.temperature - 2.0*i
			s._update()
			sensorsBelow.append(s)
	
		
func generate_heatMap():
	var min_x = sensors.map(func(s): return s.position.x).min()
	var max_x = sensors.map(func(s): return s.position.x).max()
	var min_z = sensors.map(func(s): return s.position.z).min()
	var max_z = sensors.map(func(s): return s.position.z).max()
	var max_y = 1.0
	var min_y = sensors.map(func(s): return s.sensorsBelow.map(func(b): return b.position.y).min()).min()
	
	var box_size = Vector3(max_x - min_x, max_y - min_y, max_z - min_z)
	heatmapInitialScale = box_size
	var center_position = Vector3((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
	heatMap.scale = box_size
	heatMap.transform.origin = center_position
	var meshCount = 5
	var step = Vector3(2.0, 2.0, 2.0)
	box_size = box_size - step
	while(box_size.x > 0.0 and box_size.y > 0.0 and box_size.z > 0.0):
		var new_mesh = heatMap.duplicate()
		new_mesh.scale = box_size
		box_size = box_size - step
		add_child(new_mesh)


func _process(delta):
	var data = PackedFloat32Array()
	for sensor in sensors:
		var position = sensor.position
		var temperature = sensor.temperature
		sensor._update()
		data.append(position.x)
		data.append(position.y)
		data.append(position.z)
		data.append(temperature)
	for sensor in sensorsBelow:
		var position = sensor.position
		var temperature = sensor.temperature
		sensor._update()
		data.append(position.x)
		data.append(position.y)
		data.append(position.z)
		data.append(temperature)
	if heatMap.get_active_material(0):
		heatMap.get_active_material(0).set_shader_parameter("sensors", data)
		heatMap.get_active_material(0).set_shader_parameter("sensor_count", sensors.size() + sensorsBelow.size())

func processRmq(sensorName, temperature):
	for sensor in sensors:
		if (sensor.name == sensorName): 
			sensor.temperature = temperature
			sensor._update()
			break;
			
func getTemperatures(sensorName):
	
	for sensor in sensors:
		if (sensor.name == sensorName):
			return JSON.stringify(sensor.sensorsBelow.map(func(s): return s.temperature+273.15))	
			
func getDepths(sensorName):
	var maxDepthInMeters = 10.0	
	for sensor in sensors:
		if (sensor.name == sensorName):
			return JSON.stringify(sensor.sensorsBelow.map(func(s): return abs((2.0/15.0)*s.pos.y*0.95)))

func updateTemperatures(sensorName, surfaceTemperature, belowTemperatures):
	for sensor in sensors:
		if (sensor.name == sensorName):
			sensor.temperature = surfaceTemperature
			sensor._update()
			for i in range(belowTemperatures.size()):
				sensor.sensorsBelow[i].temperature = belowTemperatures[i]
				sensorsBelow[i]._update()
	print(sensorName + " : " + str(surfaceTemperature))

func _on_heatmap_size_drag_ended(value_changed: bool) -> void:
	heatMap.scale = heatmapInitialScale * $Settings/MarginContainer/VBoxContainer/HeatmapSize.value
