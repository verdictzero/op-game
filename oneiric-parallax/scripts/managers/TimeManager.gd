extends Node
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
