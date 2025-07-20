extends Control
class_name MainMenu

signal new_game_requested()
signal quit_requested()

@onready var new_game_button = $VBox/NewGameButton
@onready var quit_button = $VBox/QuitButton
@onready var title_label = $VBox/TitleLabel

func _ready():
	setup_ui()

func setup_ui():
	new_game_button.pressed.connect(_on_new_game_pressed)
	quit_button.pressed.connect(_on_quit_pressed)
	
	# Animate title
	title_label.modulate.a = 0.0
	var tween = create_tween()
	tween.tween_property(title_label, "modulate:a", 1.0, 1.0)

func _on_new_game_pressed():
	print("New game button pressed")
	new_game_requested.emit()

func _on_quit_pressed():
	print("Quit button pressed")
	quit_requested.emit()

func _input(event):
	if event.is_action_pressed("ui_cancel"):
		get_tree().quit()