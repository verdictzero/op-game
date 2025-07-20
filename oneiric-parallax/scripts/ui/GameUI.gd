extends Control
class_name GameUI

@onready var god_powers_panel = $GodPowersPanel
@onready var fire_count_label = $GodPowersPanel/VBox/FireCountLabel
@onready var instructions_label = $GodPowersPanel/VBox/InstructionsLabel

@onready var world_info_panel = $WorldInfoPanel
@onready var world_stats_label = $WorldInfoPanel/VBox/WorldStatsLabel

var fire_system: FireSystemSimple

func _ready():
	setup_ui()

func setup_ui():
	instructions_label.text = "GOD POWERS:\nLeft Click: Start Fire\nRight Click: Spawn Units\nWASD: Move Camera\nMouse Wheel: Zoom\nESC: Main Menu"

func set_fire_system(fs: FireSystemSimple):
	fire_system = fs

func _process(_delta):
	update_fire_count()

func update_fire_count():
	if fire_system:
		fire_count_label.text = "Active Fires: %d" % fire_system.get_fire_count()

func set_world_stats(stats: Dictionary):
	var stats_text = "WORLD INFO:\n"
	stats_text += "Size: %dx%d\n" % [stats.get("world_width", 0), stats.get("world_height", 0)]
	stats_text += "Terrain Types: %d\n" % stats.terrain_counts.size()
	stats_text += "Resources: %d types\n" % stats.resource_counts.size()
	
	world_stats_label.text = stats_text

func show_god_powers():
	god_powers_panel.visible = true

func hide_god_powers():
	god_powers_panel.visible = false

func show_world_info():
	world_info_panel.visible = true

func hide_world_info():
	world_info_panel.visible = false