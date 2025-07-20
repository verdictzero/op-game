extends Control
class_name GameUI

@onready var god_powers_panel = $GodPowersPanel
@onready var fire_count_label = $GodPowersPanel/VBox/FireCountLabel
@onready var instructions_label = $GodPowersPanel/VBox/InstructionsLabel

@onready var world_info_panel = $WorldInfoPanel
@onready var world_stats_label = $WorldInfoPanel/VBox/WorldStatsLabel

var fire_system: FireSystemSimple
var is_generating = false

func _ready():
	setup_ui()

func setup_ui():
	instructions_label.text = "GOD POWERS:\nLeft Click: Start Fire\nRight Click: Spawn Units\nWASD: Move Camera\nMouse Wheel: Zoom\nESC: Main Menu"
	world_stats_label.text = "Generating world..."

func set_fire_system(fs: FireSystemSimple):
	fire_system = fs

func _process(_delta):
	if not is_generating:
		update_fire_count()

func update_fire_count():
	if fire_system:
		fire_count_label.text = "Active Fires: %d" % fire_system.get_fire_count()

func update_generation_progress(progress: float, message: String):
	is_generating = true
	var progress_text = "GENERATING WORLD:\n"
	progress_text += "%s\n" % message
	progress_text += "Progress: %.1f%%" % (progress * 100)
	world_stats_label.text = progress_text

func on_world_generation_complete():
	is_generating = false

func update_world_stats(stats: Dictionary):
	var stats_text = "WORLD INFO:\n"
	stats_text += "Size: %dx%d tiles\n" % [stats.get("world_width", 128), stats.get("world_height", 128)]
	stats_text += "Total tiles: %d\n" % stats.get("total_tiles", 0)
	stats_text += "\nTERRAIN:\n"
	
	for terrain in stats.terrain_counts.keys():
		var count = stats.terrain_counts[terrain]
		var percentage = (count * 100.0) / stats.total_tiles
		stats_text += "%s: %.1f%%\n" % [terrain.capitalize(), percentage]
	
	stats_text += "\nRESOURCES:\n"
	for resource in stats.resource_counts.keys():
		stats_text += "%s: %d\n" % [resource.capitalize(), stats.resource_counts[resource]]
	
	world_stats_label.text = stats_text

func show_god_powers():
	god_powers_panel.visible = true

func hide_god_powers():
	god_powers_panel.visible = false

func show_world_info():
	world_info_panel.visible = true

func hide_world_info():
	world_info_panel.visible = false