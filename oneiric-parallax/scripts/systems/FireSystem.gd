extends Node
class_name FireSystem

signal fire_started(position: Vector2)
signal fire_spread(from: Vector2, to: Vector2)
signal fire_extinguished(position: Vector2)

var active_fires: Array[Fire] = []
var world_generator: WorldGenerator
var world_container: Node2D

var spread_chance: float = 0.3
var extinguish_chance: float = 0.1
var growth_rate: float = 0.5
var spread_distance: float = 64.0  # 2 tiles

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
		if randf() < extinguish_chance * delta:
			extinguish_fire(fire)
			fires_to_remove.append(fire)
	
	# Remove extinguished fires
	for fire in fires_to_remove:
		active_fires.erase(fire)

func start_fire(world_pos: Vector2, intensity: Fire.Intensity = Fire.Intensity.SMALL):
	# Check if there's already a fire nearby
	for existing_fire in active_fires:
		if existing_fire.position.distance_to(world_pos) < 32.0:
			return  # Too close to existing fire
	
	var fire = Fire.new()
	fire.setup(world_pos, intensity, world_container)
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
		start_fire(target_pos, Fire.Intensity.IGNITION)
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
	print("Fire extinguished at: ", fire.position)

func extinguish_all_fires():
	for fire in active_fires:
		extinguish_fire(fire)
	active_fires.clear()

func get_fire_count() -> int:
	return active_fires.size()

class Fire:
	enum Intensity {
		IGNITION,
		SMALL,
		MEDIUM,
		LARGE,
		DYING
	}
	
	var position: Vector2
	var intensity: Intensity
	var age: float = 0.0
	var max_age: float = 30.0  # seconds
	
	var fire_sprite: AnimatedSprite2D
	var smoke_sprite: AnimatedSprite2D
	var ember_sprite: AnimatedSprite2D
	
	func setup(pos: Vector2, initial_intensity: Intensity, container: Node2D):
		position = pos
		intensity = initial_intensity
		
		create_visual_effects(container)
		update_intensity_visuals()
	
	func create_visual_effects(container: Node2D):
		# Create fire sprite
		fire_sprite = AnimatedSprite2D.new()
		fire_sprite.position = position
		container.add_child(fire_sprite)
		
		# Create fire animation frames
		var fire_animation = SpriteFrames.new()
		fire_animation.add_animation("burn")
		
		# Add fire frames for current intensity
		for frame in range(4):
			var texture_path = "res://sprites/fire/fire_%s_frame_%d.png" % [get_intensity_name(), frame]
			var texture = load(texture_path)
			if texture:
				fire_animation.add_frame("burn", texture)
		
		fire_sprite.sprite_frames = fire_animation
		fire_sprite.play("burn")
		
		# Create smoke effect (appears after fire grows)
		if intensity != Intensity.IGNITION:
			smoke_sprite = AnimatedSprite2D.new()
			smoke_sprite.position = position + Vector2(0, -16)
			container.add_child(smoke_sprite)
			
			var smoke_animation = SpriteFrames.new()
			smoke_animation.add_animation("drift")
			
			for frame in range(8):
				var smoke_texture = load("res://sprites/fire/smoke_frame_%d.png" % frame)
				if smoke_texture:
					smoke_animation.add_frame("drift", smoke_texture)
			
			smoke_sprite.sprite_frames = smoke_animation
			smoke_sprite.play("drift")
		
		# Create ember effects for larger fires
		if intensity in [Intensity.MEDIUM, Intensity.LARGE]:
			ember_sprite = AnimatedSprite2D.new()
			ember_sprite.position = position + Vector2(randf_range(-16, 16), randf_range(-16, 16))
			container.add_child(ember_sprite)
			
			var ember_animation = SpriteFrames.new()
			ember_animation.add_animation("glow")
			
			for frame in range(6):
				var ember_texture = load("res://sprites/fire/ember_frame_%d.png" % frame)
				if ember_texture:
					ember_animation.add_frame("glow", ember_texture)
			
			ember_sprite.sprite_frames = ember_animation
			ember_sprite.play("glow")
	
	func update(delta: float):
		age += delta
		
		# Fire lifecycle progression
		var age_ratio = age / max_age
		if age_ratio < 0.2:
			set_intensity(Intensity.IGNITION)
		elif age_ratio < 0.4:
			set_intensity(Intensity.SMALL)
		elif age_ratio < 0.6:
			set_intensity(Intensity.MEDIUM)
		elif age_ratio < 0.8:
			set_intensity(Intensity.LARGE)
		else:
			set_intensity(Intensity.DYING)
	
	func set_intensity(new_intensity: Intensity):
		if intensity != new_intensity:
			intensity = new_intensity
			update_intensity_visuals()
	
	func update_intensity_visuals():
		if fire_sprite and fire_sprite.sprite_frames:
			# Update fire animation with new intensity frames
			var animation = fire_sprite.sprite_frames
			animation.clear("burn")
			
			for frame in range(4):
				var texture_path = "res://sprites/fire/fire_%s_frame_%d.png" % [get_intensity_name(), frame]
				var texture = load(texture_path)
				if texture:
					animation.add_frame("burn", texture)
	
	func get_intensity_name() -> String:
		match intensity:
			Intensity.IGNITION:
				return "ignition"
			Intensity.SMALL:
				return "small"
			Intensity.MEDIUM:
				return "medium"
			Intensity.LARGE:
				return "large"
			Intensity.DYING:
				return "dying"
		return "small"
	
	func extinguish():
		if fire_sprite:
			fire_sprite.queue_free()
		if smoke_sprite:
			smoke_sprite.queue_free()
		if ember_sprite:
			ember_sprite.queue_free()