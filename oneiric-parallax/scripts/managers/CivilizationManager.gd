extends Node
class_name CivilizationManager

var civilizations: Array[Civilization]
var next_civ_id: int = 0

func spawn_initial_civilizations(container: Node2D):
	# Spawn a few primitive civilizations
	for i in range(3):
		spawn_civilization("primitive", container)

func spawn_civilization(era: String, container: Node2D):
	var civ = Civilization.new()
	civ.id = next_civ_id
	civ.era = era
	civ.spawn_position = get_random_spawn_position()
	
	civilizations.append(civ)
	next_civ_id += 1
	
	# Spawn initial units
	spawn_initial_units(civ, container)

func spawn_initial_units(civ: Civilization, container: Node2D):
	var unit_scene = preload("res://scenes/entities/Unit.tscn")
	
	for i in range(5):  # Start with 5 units
		var unit = unit_scene.instantiate()
		unit.position = civ.spawn_position + Vector2(randf_range(-50, 50), randf_range(-50, 50))
		unit.civilization_id = civ.id
		unit.set_sprite_for_era(civ.era, "basic")
		
		container.add_child(unit)
		civ.units.append(unit)

func get_random_spawn_position() -> Vector2:
	return Vector2(randf_range(100, 900), randf_range(100, 900))

func _process(delta):
	update_civilizations(delta)

func update_civilizations(delta):
	for civ in civilizations:
		civ.update(delta)

class Civilization:
	var id: int
	var era: String
	var spawn_position: Vector2
	var units: Array[Unit]
	var buildings: Array[Building]
	var technologies: Array[String]
	var resources: Dictionary
	
	func _init():
		units = []
		buildings = []
		technologies = []
		resources = {"food": 100, "wood": 50, "stone": 25}
	
	func update(delta: float):
		# Update civilization-level AI
		process_technology_research(delta)
		manage_resources(delta)
	
	func process_technology_research(delta: float):
		# Simple tech progression
		pass
	
	func manage_resources(delta: float):
		# Resource management
		pass
