extends Node3D
class_name Borehole
@export var depth: int = 10
@export var sensor_count: int = 5
@export var sensor_scene: PackedScene
var sensors = []

func _ready() -> void:
	var x = position.x
	var z = position.z
	var step = float(depth) / float(sensor_count)
	for i in range(sensor_count + 1):
		var sensor = sensor_scene.instantiate() as Sensor
		sensor.position = Vector3(x, -i * step, z)
		sensors.append(sensor)
