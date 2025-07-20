extends Control
class_name WorldGenUI

signal generate_world_requested(params: Dictionary)
signal start_game_requested()

@onready var world_size_slider = $ScrollContainer/VBox/MainContainer/LeftColumn/WorldSizeContainer/WorldSizeSlider
@onready var world_size_label = $ScrollContainer/VBox/MainContainer/LeftColumn/WorldSizeContainer/WorldSizeLabel
@onready var seed_input = $ScrollContainer/VBox/MainContainer/LeftColumn/SeedContainer/SeedInput
@onready var random_seed_button = $ScrollContainer/VBox/MainContainer/LeftColumn/SeedContainer/RandomSeedButton

@onready var temperature_slider = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/TemperatureContainer/TemperatureSlider
@onready var temperature_label = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/TemperatureContainer/TemperatureLabel
@onready var humidity_slider = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/HumidityContainer/HumiditySlider
@onready var humidity_label = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/HumidityContainer/HumidityLabel
@onready var elevation_slider = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/ElevationContainer/ElevationSlider
@onready var elevation_label = $ScrollContainer/VBox/MainContainer/LeftColumn/ClimateContainer/ElevationContainer/ElevationLabel

@onready var resource_slider = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/ResourceDensityContainer/ResourceSlider
@onready var resource_label = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/ResourceDensityContainer/ResourceLabel
@onready var vegetation_slider = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/VegetationContainer/VegetationSlider
@onready var vegetation_label = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/VegetationContainer/VegetationLabel
@onready var river_slider = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/RiverContainer/RiverSlider
@onready var river_label = $ScrollContainer/VBox/MainContainer/RightColumn/ResourcesContainer/RiverContainer/RiverLabel

@onready var generate_button = $ScrollContainer/VBox/ButtonContainer/GenerateButton
@onready var start_game_button = $ScrollContainer/VBox/ButtonContainer/StartGameButton
@onready var presets_option = $ScrollContainer/VBox/MainContainer/LeftColumn/PresetsContainer/PresetsOption

@onready var progress_container = $ScrollContainer/VBox/MainContainer/RightColumn/ProgressContainer
@onready var progress_bar = $ScrollContainer/VBox/MainContainer/RightColumn/ProgressContainer/ProgressBar
@onready var progress_label = $ScrollContainer/VBox/MainContainer/RightColumn/ProgressContainer/ProgressLabel

@onready var stats_container = $ScrollContainer/VBox/MainContainer/RightColumn/StatsContainer
@onready var stats_label = $ScrollContainer/VBox/MainContainer/RightColumn/StatsContainer/StatsLabel

var world_generator: WorldGenerator

func _ready():
	setup_ui()
	setup_presets()
	update_labels()
	hide_progress()
	hide_stats()

func setup_ui():
	# Connect signals
	world_size_slider.value_changed.connect(_on_world_size_changed)
	random_seed_button.pressed.connect(_on_random_seed_pressed)
	temperature_slider.value_changed.connect(_on_temperature_changed)
	humidity_slider.value_changed.connect(_on_humidity_changed)
	elevation_slider.value_changed.connect(_on_elevation_changed)
	resource_slider.value_changed.connect(_on_resource_changed)
	vegetation_slider.value_changed.connect(_on_vegetation_changed)
	river_slider.value_changed.connect(_on_river_changed)
	generate_button.pressed.connect(_on_generate_pressed)
	start_game_button.pressed.connect(_on_start_game_pressed)
	presets_option.item_selected.connect(_on_preset_selected)
	
	# Set initial values  
	world_size_slider.value = 64  # Match WorldGenerator default
	seed_input.text = str(randi())
	temperature_slider.value = 0.1
	humidity_slider.value = 0.15
	elevation_slider.value = 0.08
	resource_slider.value = 0.3
	vegetation_slider.value = 0.4
	river_slider.value = 3
	
	start_game_button.disabled = true

func setup_presets():
	presets_option.add_item("Custom")
	presets_option.add_item("Earth-like")
	presets_option.add_item("Desert World")
	presets_option.add_item("Ocean World")
	presets_option.add_item("Mountain World")
	presets_option.add_item("Forest World")
	presets_option.add_item("Volcanic World")

func update_labels():
	world_size_label.text = "World Size: %dx%d" % [int(world_size_slider.value), int(world_size_slider.value)]
	temperature_label.text = "Temperature Scale: %.2f" % temperature_slider.value
	humidity_label.text = "Humidity Scale: %.2f" % humidity_slider.value
	elevation_label.text = "Elevation Scale: %.2f" % elevation_slider.value
	resource_label.text = "Resource Density: %.1f%%" % (resource_slider.value * 100)
	vegetation_label.text = "Vegetation Density: %.1f%%" % (vegetation_slider.value * 100)
	river_label.text = "Rivers: %d" % int(river_slider.value)

func _on_world_size_changed(value: float):
	update_labels()

func _on_random_seed_pressed():
	seed_input.text = str(randi())

func _on_temperature_changed(value: float):
	update_labels()
	presets_option.selected = 0  # Set to custom

func _on_humidity_changed(value: float):
	update_labels()
	presets_option.selected = 0

func _on_elevation_changed(value: float):
	update_labels()
	presets_option.selected = 0

func _on_resource_changed(value: float):
	update_labels()
	presets_option.selected = 0

func _on_vegetation_changed(value: float):
	update_labels()
	presets_option.selected = 0

func _on_river_changed(value: float):
	update_labels()
	presets_option.selected = 0

func _on_preset_selected(index: int):
	var preset_name = presets_option.get_item_text(index)
	apply_preset(preset_name)

func apply_preset(preset_name: String):
	match preset_name:
		"Earth-like":
			temperature_slider.value = 0.1
			humidity_slider.value = 0.15
			elevation_slider.value = 0.08
			resource_slider.value = 0.3
			vegetation_slider.value = 0.4
			river_slider.value = 5
		"Desert World":
			temperature_slider.value = 0.05
			humidity_slider.value = 0.05
			elevation_slider.value = 0.12
			resource_slider.value = 0.1
			vegetation_slider.value = 0.1
			river_slider.value = 1
		"Ocean World":
			temperature_slider.value = 0.08
			humidity_slider.value = 0.2
			elevation_slider.value = 0.04
			resource_slider.value = 0.4
			vegetation_slider.value = 0.2
			river_slider.value = 8
		"Mountain World":
			temperature_slider.value = 0.12
			humidity_slider.value = 0.1
			elevation_slider.value = 0.15
			resource_slider.value = 0.5
			vegetation_slider.value = 0.3
			river_slider.value = 3
		"Forest World":
			temperature_slider.value = 0.08
			humidity_slider.value = 0.2
			elevation_slider.value = 0.06
			resource_slider.value = 0.4
			vegetation_slider.value = 0.8
			river_slider.value = 6
		"Volcanic World":
			temperature_slider.value = 0.15
			humidity_slider.value = 0.08
			elevation_slider.value = 0.2
			resource_slider.value = 0.6
			vegetation_slider.value = 0.2
			river_slider.value = 2
	
	update_labels()

func _on_generate_pressed():
	var params = {
		"world_size": Vector2i(int(world_size_slider.value), int(world_size_slider.value)),
		"seed": int(seed_input.text) if seed_input.text.is_valid_int() else randi(),
		"temperature_scale": temperature_slider.value,
		"humidity_scale": humidity_slider.value,
		"elevation_scale": elevation_slider.value,
		"resource_density": resource_slider.value,
		"vegetation_density": vegetation_slider.value,
		"river_count": int(river_slider.value)
	}
	
	show_progress()
	hide_stats()
	generate_button.disabled = true
	start_game_button.disabled = true
	
	generate_world_requested.emit(params)

func _on_start_game_pressed():
	start_game_requested.emit()

func show_progress():
	progress_container.visible = true

func hide_progress():
	progress_container.visible = false

func show_stats():
	stats_container.visible = true

func hide_stats():
	stats_container.visible = false

func update_progress(progress: float, message: String):
	progress_bar.value = progress * 100
	progress_label.text = message

func on_generation_complete():
	hide_progress()
	generate_button.disabled = false
	start_game_button.disabled = false

func display_world_stats(stats: Dictionary):
	show_stats()
	
	var stats_text = "World Statistics:\n"
	stats_text += "Total Tiles: %d\n" % stats.total_tiles
	stats_text += "Avg Elevation: %.2f\n" % stats.avg_elevation
	stats_text += "Avg Temperature: %.2f\n" % stats.avg_temperature
	stats_text += "Avg Humidity: %.2f\n\n" % stats.avg_humidity
	
	stats_text += "Terrain Distribution:\n"
	for terrain in stats.terrain_counts:
		var count = stats.terrain_counts[terrain]
		var percentage = (float(count) / stats.total_tiles) * 100
		stats_text += "- %s: %d (%.1f%%)\n" % [terrain.capitalize(), count, percentage]
	
	if stats.resource_counts.size() > 0:
		stats_text += "\nResources Found:\n"
		for resource in stats.resource_counts:
			stats_text += "- %s: %d locations\n" % [resource.capitalize(), stats.resource_counts[resource]]
	
	stats_label.text = stats_text

func set_world_generator(generator: WorldGenerator):
	world_generator = generator
	if world_generator:
		world_generator.generation_progress.connect(update_progress)
		world_generator.generation_complete.connect(on_generation_complete)