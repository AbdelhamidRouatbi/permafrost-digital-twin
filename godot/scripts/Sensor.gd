extends Node3D
class_name Sensor

@export var temperature: float = -30.0
var sensorsBelow: Array[Sensor] = []

func _update():
	_update_label()

func _update_label():
	var label = get_node("SensorLabel") as Label3D
	if label:
		label.text = "%.2f°C" % temperature

func _ready():
	_update()
