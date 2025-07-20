extends Node
class_name FireSystemSimple

signal fire_started(position: Vector2)
signal fire_spread(from: Vector2, to: Vector2)
signal fire_extinguished(position: Vector2)

var active_fires: Array[Fire] = []
var world_generator: WorldGenerator
var world_container: Node2D

var spread_chance: float = 0.2
var extinguish_chance: float = 0.05
var spread_distance: float = 64.0

func _ready():
	set_process(true)

func setup(generator: WorldGenerator, container: Node2D):
	world_generator = generator
	world_container = container

func _process(delta):
	update_fires(delta)

func update_fires(delta):
	var fires_to_remove = []
	
	for fire in active_fires:
		fire.update(delta)
		
		# Check if fire should spread
		if randf() < spread_chance * delta:
			attempt_fire_spread(fire)
		
		# Check if fire should extinguish
		if randf() < extinguish_chance * delta or fire.age > fire.max_age:
			extinguish_fire(fire)
			fires_to_remove.append(fire)
	
	# Remove extinguished fires
	for fire in fires_to_remove:
		active_fires.erase(fire)

func start_fire(world_pos: Vector2):
	# Check if there's already a fire nearby
	for existing_fire in active_fires:
		if existing_fire.position.distance_to(world_pos) < 32.0:
			return  # Too close to existing fire
	
	var fire = Fire.new()
	fire.setup(world_pos, world_container)
	active_fires.append(fire)
	
	fire_started.emit(world_pos)
	print("Fire started at: ", world_pos)

func attempt_fire_spread(fire: Fire):
	# Get nearby positions to spread to
	var spread_positions = get_spreadable_positions(fire.position)
	
	if spread_positions.is_empty():
		return
	
	var target_pos = spread_positions[randi() % spread_positions.size()]
	
	# Check if vegetation is flammable at target position
	if is_position_flammable(target_pos):
		start_fire(target_pos)
		fire_spread.emit(fire.position, target_pos)

func get_spreadable_positions(from_pos: Vector2) -> Array[Vector2]:
	var positions = []
	var directions = [
		Vector2(32, 0), Vector2(-32, 0), Vector2(0, 32), Vector2(0, -32),
		Vector2(32, 32), Vector2(-32, -32), Vector2(32, -32), Vector2(-32, 32)
	]
	
	for direction in directions:
		var target_pos = from_pos + direction
		if is_valid_spread_position(target_pos):
			positions.append(target_pos)
	
	return positions

func is_valid_spread_position(pos: Vector2) -> bool:
	# Check if position is within world bounds
	if not world_generator:
		return false
	
	var tile_x = int(pos.x / 32)
	var tile_y = int(pos.y / 32)
	
	if tile_x < 0 or tile_x >= world_generator.world_size.x or tile_y < 0 or tile_y >= world_generator.world_size.y:
		return false
	
	# Check if there's already a fire there
	for existing_fire in active_fires:
		if existing_fire.position.distance_to(pos) < 16.0:
			return false
	
	return true

func is_position_flammable(pos: Vector2) -> bool:
	if not world_generator:
		return false
	
	var tile_x = int(pos.x / 32)
	var tile_y = int(pos.y / 32)
	
	if tile_x < 0 or tile_x >= world_generator.world_size.x or tile_y < 0 or tile_y >= world_generator.world_size.y:
		return false
	
	var tile_data = world_generator.world_data[tile_x][tile_y]
	var terrain_type = tile_data.get("terrain_type", "")
	var vegetation = tile_data.get("vegetation", [])
	
	# Flammable terrain types
	if terrain_type in ["forest", "grass", "swamp"]:
		return true
	
	# Vegetation makes terrain flammable
	if not vegetation.is_empty():
		return true
	
	return false

func extinguish_fire(fire: Fire):
	fire.extinguish()
	fire_extinguished.emit(fire.position)

func extinguish_all_fires():
	for fire in active_fires:
		extinguish_fire(fire)
	active_fires.clear()

func get_fire_count() -> int:
	return active_fires.size()

class Fire:
	var position: Vector2
	var age: float = 0.0
	var max_age: float = 15.0  # seconds
	
	var fire_sprite: Sprite2D
	
	func setup(pos: Vector2, container: Node2D):
		position = pos
		create_visual_effects(container)
	
	func create_visual_effects(container: Node2D):
		# Create simple fire sprite
		fire_sprite = Sprite2D.new()
		fire_sprite.position = position
		
		# Try to load fire texture
		var fire_texture = load("res://sprites/fire/fire_medium_frame_0.png")
		if fire_texture:
			fire_sprite.texture = fire_texture
		else:
			# Fallback: create a colored rectangle
			var rect = ReferenceRect.new()
			rect.position = position
			rect.size = Vector2(32, 32)
			rect.border_color = Color.RED
			container.add_child(rect)
			return
		
		container.add_child(fire_sprite)
	
	func update(delta: float):
		age += delta
		
		# Simple flickering effect
		if fire_sprite:
			var flicker = sin(age * 10.0) * 0.2 + 1.0
			fire_sprite.modulate = Color(1.0, flicker, 0.0)
	
	func extinguish():
		if fire_sprite:
			fire_sprite.queue_free()