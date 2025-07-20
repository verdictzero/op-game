extends CharacterBody2D
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
