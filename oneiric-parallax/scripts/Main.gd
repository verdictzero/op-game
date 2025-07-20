extends Node2D

@onready var camera = $Camera2D
@onready var world_container = $WorldContainer
@onready var entity_container = $EntityContainer
@onready var game_ui = $UI/GameUI

var world_generator: WorldGenerator
var civilization_manager: CivilizationManager
var time_manager: TimeManager

var camera_speed = 300.0
var zoom_speed = 0.1
var world_bounds: Rect2

func _ready():
	setup_managers()
	generate_initial_world()

func setup_managers():
	world_generator = WorldGenerator.new()
	civilization_manager = CivilizationManager.new()
	time_manager = TimeManager.new()
	
	add_child(world_generator)
	add_child(civilization_manager)
	add_child(time_manager)
	
	# Connect world generator signals
	world_generator.generation_progress.connect(_on_generation_progress)
	world_generator.generation_complete.connect(_on_generation_complete)

func generate_initial_world():
	# Set world bounds based on world size
	var world_size = world_generator.world_size
	var tile_size = world_generator.tile_size
	world_bounds = Rect2(0, 0, world_size.x * tile_size, world_size.y * tile_size)
	
	# Position camera at center of world
	camera.position = Vector2(world_bounds.size.x / 2, world_bounds.size.y / 2)
	
	# Generate world asynchronously
	world_generator.generate_world_async(world_container)

func _on_generation_progress(progress: float, message: String):
	if game_ui:
		game_ui.update_generation_progress(progress, message)

func _on_generation_complete():
	if game_ui:
		game_ui.on_world_generation_complete()
		# Update world stats
		var stats = world_generator.get_world_stats()
		game_ui.update_world_stats(stats)
	
	# Spawn civilizations after world generation
	civilization_manager.spawn_initial_civilizations(entity_container)
	
	# Setup fire system
	setup_fire_system()

func setup_fire_system():
	var fire_system = FireSystemSimple.new()
	add_child(fire_system)
	
	if game_ui:
		game_ui.set_fire_system(fire_system)

func _input(event):
	handle_camera_controls(event)
	handle_god_powers(event)

func handle_camera_controls(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			camera.zoom *= (1.0 + zoom_speed)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			camera.zoom *= (1.0 - zoom_speed)

func handle_god_powers(event):
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_LEFT:
			var world_pos = camera.get_global_mouse_position()
			# Handle god power activation
			pass

func _process(delta):
	handle_camera_movement(delta)

func handle_camera_movement(delta):
	var input_vector = Vector2()
	
	# Use WASD keys for camera movement
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		input_vector.x -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		input_vector.x += 1
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		input_vector.y -= 1
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		input_vector.y += 1
	
	if input_vector.length() > 0:
		var movement = input_vector.normalized() * camera_speed * delta / camera.zoom.x
		var new_position = camera.position + movement
		
		# Constrain camera to world bounds with some padding
		var viewport_size = get_viewport().get_visible_rect().size / camera.zoom
		var padding = viewport_size * 0.1  # 10% padding
		
		new_position.x = clamp(new_position.x, -padding.x, world_bounds.size.x + padding.x)
		new_position.y = clamp(new_position.y, -padding.y, world_bounds.size.y + padding.y)
		
		camera.position = new_position
