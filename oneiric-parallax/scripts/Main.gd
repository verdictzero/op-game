extends Node2D

@onready var camera = $Camera2D
@onready var world_container = $WorldContainer
@onready var entity_container = $EntityContainer

var world_generator: WorldGenerator
var civilization_manager: CivilizationManager
var time_manager: TimeManager

var camera_speed = 300.0
var zoom_speed = 0.1

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

func generate_initial_world():
    world_generator.generate_world(world_container)
    civilization_manager.spawn_initial_civilizations(entity_container)

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
    
    if Input.is_action_pressed("move_camera_left"):
        input_vector.x -= 1
    if Input.is_action_pressed("move_camera_right"):
        input_vector.x += 1
    if Input.is_action_pressed("move_camera_up"):
        input_vector.y -= 1
    if Input.is_action_pressed("move_camera_down"):
        input_vector.y += 1
    
    if input_vector.length() > 0:
        camera.position += input_vector.normalized() * camera_speed * delta / camera.zoom.x
