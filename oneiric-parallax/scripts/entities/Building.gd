extends StaticBody2D
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
