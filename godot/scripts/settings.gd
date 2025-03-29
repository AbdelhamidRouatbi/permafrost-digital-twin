extends Control

func _ready() -> void:
	$MarginContainer/VBoxContainer/Temperature_Inc.visible = false

func _on_check_button_toggled(toggled_on: bool) -> void:
	if(toggled_on):
		$MarginContainer/VBoxContainer/Temperature_Inc.visible = false
	else:
		$MarginContainer/VBoxContainer/Temperature_Inc.visible = true


func _on_increment_value_changed(value: float) -> void:
	$MarginContainer/VBoxContainer/Temperature_Inc/Label_IncValue.text = str(value)
