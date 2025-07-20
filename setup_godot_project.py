#!/usr/bin/env python3
"""
Godot Project Setup Script
Sets up the basic project structure for the cosmic civilization game
"""

import os
import json
from pathlib import Path

PROJECT_DIR = Path("oneiric-parallax")

# Godot project structure
DIRECTORIES = [
    "scripts",
    "scripts/systems",
    "scripts/entities",
    "scripts/ui",
    "scripts/managers",
    "scenes",
    "scenes/entities",
    "scenes/ui",
    "scenes/world",
    "sprites",
    "sprites/primitive",
    "sprites/industrial", 
    "sprites/space",
    "sprites/terrain",
    "sprites/effects",
    "audio",
    "audio/sfx",
    "audio/music",
    "data",
    "data/civilizations",
    "data/technologies",
    "shaders"
]

# Godot scene templates
SCENE_TEMPLATES = {
    "Main.tscn": """[gd_scene load_steps=2 format=3 uid="uid://b3qxkw8qv2yx5"]

[ext_resource type="Script" path="res://scripts/Main.gd" id="1_0jxkw"]

[node name="Main" type="Node2D"]
script = ExtResource("1_0jxkw")

[node name="Camera2D" type="Camera2D" parent="."]
zoom = Vector2(2, 2)

[node name="UI" type="CanvasLayer" parent="."]

[node name="WorldContainer" type="Node2D" parent="."]

[node name="EntityContainer" type="Node2D" parent="."]
""",

    "scenes/entities/Unit.tscn": """[gd_scene load_steps=3 format=3 uid="uid://b8j5n7w2x4k9m"]

[ext_resource type="Script" path="res://scripts/entities/Unit.gd" id="1_2hjkl"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_1"]
size = Vector2(8, 8)

[node name="Unit" type="CharacterBody2D"]
script = ExtResource("1_2hjkl")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture_filter = 0

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_1")

[node name="AI" type="Node" parent="."]

[node name="Needs" type="Node" parent="."]
""",

    "scenes/entities/Building.tscn": """[gd_scene load_steps=3 format=3 uid="uid://c9k6m8n5p2q7r"]

[ext_resource type="Script" path="res://scripts/entities/Building.gd" id="1_3klmn"]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_1"]
size = Vector2(16, 16)

[node name="Building" type="StaticBody2D"]
script = ExtResource("1_3klmn")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture_filter = 0

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
shape = SubResource("RectangleShape2D_1")

[node name="ProductionArea" type="Area2D" parent="."]
""",

    "scenes/world/TerrainTile.tscn": """[gd_scene load_steps=2 format=3 uid="uid://d4l7n9o6q3r8s"]

[ext_resource type="Script" path="res://scripts/world/TerrainTile.gd" id="1_4mnop"]

[node name="TerrainTile" type="Sprite2D"]
texture_filter = 0
script = ExtResource("1_4mnop")
"""
}

# GDScript templates
SCRIPT_TEMPLATES = {
    "scripts/Main.gd": '''extends Node2D

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
''',

    "scripts/entities/Unit.gd": '''extends CharacterBody2D
class_name Unit

@onready var sprite = $Sprite2D
@onready var ai_node = $AI
@onready var needs_node = $Needs

var unit_data: UnitData
var civilization_id: int
var current_needs: Array[Need]
var personality: Dictionary

var move_speed = 50.0
var current_target: Vector2
var current_action: String = ""

func _ready():
    setup_unit()

func setup_unit():
    current_needs = []
    personality = generate_personality()
    
func generate_personality() -> Dictionary:
    return {
        "aggression": randf(),
        "curiosity": randf(),
        "social": randf(),
        "innovation": randf()
    }

func _physics_process(delta):
    update_ai(delta)
    move_towards_target(delta)

func update_ai(delta):
    update_needs(delta)
    decide_action()

func update_needs(delta):
    # Update basic needs like food, safety, social
    for need in current_needs:
        need.decay(delta)

func decide_action():
    if current_needs.is_empty():
        return
        
    var most_urgent_need = get_most_urgent_need()
    current_action = determine_action_for_need(most_urgent_need)

func get_most_urgent_need() -> Need:
    var most_urgent = current_needs[0]
    for need in current_needs:
        if need.urgency > most_urgent.urgency:
            most_urgent = need
    return most_urgent

func determine_action_for_need(need: Need) -> String:
    match need.type:
        "food":
            return "seek_food"
        "safety":
            return "flee_danger"
        "social":
            return "seek_companions"
        _:
            return "wander"

func move_towards_target(delta):
    if current_target != Vector2.ZERO:
        var direction = (current_target - global_position).normalized()
        velocity = direction * move_speed
        move_and_slide()

func set_sprite_for_era(era: String, unit_type: String):
    var sprite_path = "res://sprites/%s/unit_%s.png" % [era, unit_type]
    var texture = load(sprite_path)
    if texture:
        sprite.texture = texture

class Need:
    var type: String
    var urgency: float
    var satisfaction: float
    var decay_rate: float
    
    func _init(need_type: String):
        type = need_type
        urgency = 0.0
        satisfaction = 1.0
        decay_rate = 0.1
    
    func decay(delta: float):
        satisfaction -= decay_rate * delta
        satisfaction = max(0.0, satisfaction)
        urgency = 1.0 - satisfaction

class UnitData:
    var name: String
    var era: String
    var type: String
    var health: float
    var max_health: float
''',

    "scripts/entities/Building.gd": '''extends StaticBody2D
class_name Building

@onready var sprite = $Sprite2D
@onready var production_area = $ProductionArea

var building_data: BuildingData
var civilization_id: int
var production_queue: Array[String]
var construction_progress: float = 0.0
var is_constructed: bool = false

func _ready():
    setup_building()

func setup_building():
    production_queue = []
    
func set_building_type(era: String, building_type: String):
    var sprite_path = "res://sprites/%s/building_%s.png" % [era, building_type]
    var texture = load(sprite_path)
    if texture:
        sprite.texture = texture

func _process(delta):
    if not is_constructed:
        update_construction(delta)
    else:
        process_production(delta)

func update_construction(delta):
    construction_progress += delta * 0.1  # 10 seconds to build
    if construction_progress >= 1.0:
        complete_construction()

func complete_construction():
    is_constructed = true
    modulate = Color.WHITE  # Remove construction tint

func process_production(delta):
    if not production_queue.is_empty():
        # Process production items
        pass

func add_to_production_queue(item: String):
    production_queue.append(item)

class BuildingData:
    var name: String
    var era: String
    var type: String
    var health: float
    var max_health: float
    var production_rate: float
''',

    "scripts/systems/WorldGenerator.gd": '''extends Node
class_name WorldGenerator

var terrain_tiles: Array[TerrainTile]
var world_size: Vector2i = Vector2i(100, 100)
var tile_size: int = 32

func generate_world(container: Node2D):
    print("Generating world...")
    
    for x in range(world_size.x):
        for y in range(world_size.y):
            var terrain_type = determine_terrain_type(x, y)
            create_terrain_tile(x, y, terrain_type, container)
    
    print("World generation complete!")

func determine_terrain_type(x: int, y: int) -> String:
    # Simple terrain generation
    var noise_value = sin(x * 0.1) * cos(y * 0.1)
    
    if noise_value > 0.3:
        return "mountain"
    elif noise_value > 0.1:
        return "forest"
    elif noise_value > -0.1:
        return "grass"
    elif noise_value > -0.3:
        return "desert"
    else:
        return "water"

func create_terrain_tile(x: int, y: int, terrain_type: String, container: Node2D):
    var tile_scene = preload("res://scenes/world/TerrainTile.tscn")
    var tile = tile_scene.instantiate()
    
    tile.position = Vector2(x * tile_size, y * tile_size)
    tile.setup_terrain(terrain_type)
    
    container.add_child(tile)
    terrain_tiles.append(tile)
''',

    "scripts/world/TerrainTile.gd": '''extends Sprite2D
class_name TerrainTile

var terrain_type: String
var resources: Array[String]
var fertility: float

func setup_terrain(type: String):
    terrain_type = type
    set_terrain_sprite()
    determine_resources()

func set_terrain_sprite():
    var sprite_path = "res://sprites/terrain/%s.png" % terrain_type
    var terrain_texture = load(sprite_path)
    if terrain_texture:
        texture = terrain_texture

func determine_resources():
    resources = []
    fertility = randf()
    
    match terrain_type:
        "grass":
            if randf() < 0.3:
                resources.append("food")
        "forest":
            resources.append("wood")
            if randf() < 0.2:
                resources.append("food")
        "mountain":
            if randf() < 0.4:
                resources.append("stone")
            if randf() < 0.1:
                resources.append("metal")
        "desert":
            fertility *= 0.3
        "water":
            resources.append("fish")
''',

    "scripts/managers/CivilizationManager.gd": '''extends Node
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
''',

    "scripts/managers/TimeManager.gd": '''extends Node
class_name TimeManager

var time_scale: float = 1.0
var is_paused: bool = false
var game_time: float = 0.0

func _ready():
    setup_input_actions()

func setup_input_actions():
    # Will be set up in input map
    pass

func _process(delta):
    if not is_paused:
        game_time += delta * time_scale

func set_time_scale(scale: float):
    time_scale = scale

func pause_game():
    is_paused = true

func unpause_game():
    is_paused = false

func toggle_pause():
    is_paused = not is_paused

func get_scaled_delta(base_delta: float) -> float:
    if is_paused:
        return 0.0
    return base_delta * time_scale
'''
}

# Input map configuration
INPUT_MAP = {
    "move_camera_left": [{"type": "keyboard", "scancode": 65}],  # A
    "move_camera_right": [{"type": "keyboard", "scancode": 68}], # D
    "move_camera_up": [{"type": "keyboard", "scancode": 87}],    # W
    "move_camera_down": [{"type": "keyboard", "scancode": 83}],  # S
    "toggle_pause": [{"type": "keyboard", "scancode": 32}],      # Space
    "speed_up": [{"type": "keyboard", "scancode": 43}],          # +
    "slow_down": [{"type": "keyboard", "scancode": 45}],         # -
}

def create_directories():
    """Create all necessary directories"""
    print("Creating project directories...")
    for directory in DIRECTORIES:
        dir_path = PROJECT_DIR / directory
        dir_path.mkdir(parents=True, exist_ok=True)
    print("✓ Directories created")

def create_scenes():
    """Create scene files"""
    print("Creating scene files...")
    for scene_name, scene_content in SCENE_TEMPLATES.items():
        scene_path = PROJECT_DIR / scene_name
        scene_path.parent.mkdir(parents=True, exist_ok=True)
        with open(scene_path, 'w') as f:
            f.write(scene_content)
    print("✓ Scene files created")

def create_scripts():
    """Create GDScript files"""
    print("Creating script files...")
    for script_name, script_content in SCRIPT_TEMPLATES.items():
        script_path = PROJECT_DIR / script_name
        script_path.parent.mkdir(parents=True, exist_ok=True)
        with open(script_path, 'w') as f:
            f.write(script_content)
    print("✓ Script files created")

def update_project_settings():
    """Update project.godot with our settings"""
    print("Updating project settings...")
    
    project_file = PROJECT_DIR / "project.godot"
    
    # Read existing content
    with open(project_file, 'r') as f:
        content = f.read()
    
    # Add our settings
    additional_settings = '''
[input]

move_camera_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97,"echo":false,"script":null)
]
}
move_camera_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100,"echo":false,"script":null)
]
}
move_camera_up={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119,"echo":false,"script":null)
]
}
move_camera_down={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":83,"key_label":0,"unicode":115,"echo":false,"script":null)
]
}
toggle_pause={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"echo":false,"script":null)
]
}

[rendering]

textures/canvas_textures/default_texture_filter=0
'''
    
    # Add main scene setting
    if 'run/main_scene' not in content:
        main_scene_setting = '\nrun/main_scene="res://Main.tscn"'
        # Insert after [application] section
        content = content.replace('[application]', '[application]' + main_scene_setting)
    
    # Append additional settings
    with open(project_file, 'w') as f:
        f.write(content + additional_settings)
    
    print("✓ Project settings updated")

def create_data_files():
    """Create initial data files"""
    print("Creating data files...")
    
    # Civilization templates
    civ_data = {
        "primitive": {
            "name": "Primitive Tribe",
            "era": "primitive",
            "technologies": ["fire", "tools", "language"],
            "units": ["gatherer", "hunter", "shaman"],
            "buildings": ["hut", "fire_pit", "shrine"]
        },
        "industrial": {
            "name": "Industrial Nation",
            "era": "industrial", 
            "technologies": ["steam_power", "electricity", "railways"],
            "units": ["worker", "engineer", "soldier"],
            "buildings": ["factory", "power_plant", "barracks"]
        },
        "space": {
            "name": "Space Civilization",
            "era": "space",
            "technologies": ["fusion_power", "space_travel", "terraforming"],
            "units": ["scientist", "astronaut", "engineer"],
            "buildings": ["lab", "spaceport", "habitat"]
        }
    }
    
    with open(PROJECT_DIR / "data" / "civilizations.json", 'w') as f:
        json.dump(civ_data, f, indent=2)
    
    print("✓ Data files created")

def main():
    print("Setting up Godot project structure...")
    print(f"Project directory: {PROJECT_DIR.absolute()}")
    
    create_directories()
    create_scenes()
    create_scripts()
    update_project_settings()
    create_data_files()
    
    print("\n🎉 Godot project setup complete!")
    print("\nNext steps:")
    print("1. Run the sprite generator: python sprite_generator.py")
    print("2. Open the project in Godot 4.4")
    print("3. Run the Main scene to see the basic world")
    print("\nProject structure ready for cosmic civilization development!")

if __name__ == "__main__":
    main()