extends Node
class_name GameManager

enum GameState {
	MAIN_MENU,
	WORLD_GENERATION,
	PLAYING
}

var current_state: GameState = GameState.MAIN_MENU

@onready var main_menu = $UI/MainMenu
@onready var world_gen_ui = $UI/WorldGenUI
@onready var game_ui = $UI/GameUI
@onready var game_world = $GameWorld

@onready var camera = $GameWorld/Camera2D
@onready var world_container = $GameWorld/WorldContainer
@onready var entity_container = $GameWorld/EntityContainer

var world_generator: WorldGenerator
var civilization_manager: CivilizationManager
var time_manager: TimeManager
var fire_system: FireSystemSimple

var camera_speed = 400.0
var zoom_speed = 0.1

func _ready():
	setup_managers()
	setup_ui()
	set_state(GameState.MAIN_MENU)

func setup_managers():
	world_generator = WorldGenerator.new()
	civilization_manager = CivilizationManager.new()
	time_manager = TimeManager.new()
	fire_system = FireSystemSimple.new()
	
	add_child(world_generator)
	add_child(civilization_manager)
	add_child(time_manager)
	add_child(fire_system)
	
	# Connect world generator to UI
	world_gen_ui.set_world_generator(world_generator)
	
	# Setup fire system
	fire_system.setup(world_generator, world_container)

func setup_ui():
	main_menu.new_game_requested.connect(_on_new_game_requested)
	main_menu.quit_requested.connect(_on_quit_requested)
	
	world_gen_ui.generate_world_requested.connect(_on_generate_world_requested)
	world_gen_ui.start_game_requested.connect(_on_start_game_requested)

func set_state(new_state: GameState):
	current_state = new_state
	
	# Hide all UI first
	main_menu.visible = false
	world_gen_ui.visible = false
	game_ui.visible = false
	game_world.visible = false
	
	# Show appropriate UI
	match current_state:
		GameState.MAIN_MENU:
			main_menu.visible = true
		GameState.WORLD_GENERATION:
			world_gen_ui.visible = true
		GameState.PLAYING:
			game_world.visible = true
			game_ui.visible = true
			game_ui.set_fire_system(fire_system)

func _on_new_game_requested():
	set_state(GameState.WORLD_GENERATION)

func _on_quit_requested():
	get_tree().quit()

func _on_generate_world_requested(params: Dictionary):
	world_generator.set_generation_params(params)
	world_generator.generate_world_async(world_container)
	
	# Connect to generation complete to show stats
	if not world_generator.generation_complete.is_connected(_on_world_generation_complete):
		world_generator.generation_complete.connect(_on_world_generation_complete)

func _on_world_generation_complete():
	var stats = world_generator.get_world_stats()
	world_gen_ui.display_world_stats(stats)
	# Store stats for later use in game UI
	stats["world_width"] = world_generator.world_size.x
	stats["world_height"] = world_generator.world_size.y
	game_ui.set_world_stats(stats)

func _on_start_game_requested():
	set_state(GameState.PLAYING)
	
	# Position camera at center of world
	var world_size = world_generator.world_size
	var center_pos = Vector2(world_size.x * 16, world_size.y * 16)  # 32/2 = 16
	camera.position = center_pos
	camera.zoom = Vector2(0.5, 0.5)  # Zoom out to see more of the world
	
	# Spawn initial civilizations
	civilization_manager.spawn_initial_civilizations(entity_container)

func _input(event):
	if current_state == GameState.PLAYING:
		handle_camera_controls(event)
		handle_god_powers(event)
	
	# ESC to go back to main menu
	if event.is_action_pressed("ui_cancel"):
		if current_state == GameState.WORLD_GENERATION:
			set_state(GameState.MAIN_MENU)
		elif current_state == GameState.PLAYING:
			set_state(GameState.MAIN_MENU)

func handle_camera_controls(event):
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			camera.zoom *= (1.0 + zoom_speed)
			camera.zoom = camera.zoom.clamp(Vector2(0.1, 0.1), Vector2(3.0, 3.0))
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			camera.zoom *= (1.0 - zoom_speed)
			camera.zoom = camera.zoom.clamp(Vector2(0.1, 0.1), Vector2(3.0, 3.0))

func handle_god_powers(event):
	if event is InputEventMouseButton and event.pressed:
		var world_pos = camera.get_global_mouse_position()
		
		if event.button_index == MOUSE_BUTTON_LEFT:
			# Left click: Start fire
			fire_system.start_fire(world_pos)
			print("Fire started at: ", world_pos)
		elif event.button_index == MOUSE_BUTTON_RIGHT:
			# Right click: Spawn civilization
			spawn_civilization_at(world_pos)
			print("Civilization spawned at: ", world_pos)

func _process(delta):
	if current_state == GameState.PLAYING:
		handle_camera_movement(delta)

func handle_camera_movement(delta):
	var input_vector = Vector2()
	
	if Input.is_action_pressed("ui_left"):
		input_vector.x -= 1
	if Input.is_action_pressed("ui_right"):
		input_vector.x += 1
	if Input.is_action_pressed("ui_up"):
		input_vector.y -= 1
	if Input.is_action_pressed("ui_down"):
		input_vector.y += 1
	
	if input_vector.length() > 0:
		camera.position += input_vector.normalized() * camera_speed * delta / camera.zoom.x

func spawn_civilization_at(world_pos: Vector2):
	# Create a new civilization at the specified position
	var unit_scene = preload("res://scenes/entities/Unit.tscn")
	
	for i in range(3):  # Spawn 3 units
		var unit = unit_scene.instantiate()
		unit.position = world_pos + Vector2(randf_range(-32, 32), randf_range(-32, 32))
		unit.civilization_id = civilization_manager.next_civ_id
		unit.set_sprite_for_era("primitive", "basic")
		entity_container.add_child(unit)