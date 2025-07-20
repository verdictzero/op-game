extends Sprite2D
class_name TerrainTile

var terrain_type: String
var resources: Array[String]
var fertility: float
var elevation: float
var temperature: float
var humidity: float
var vegetation: Array[String]

var vegetation_sprites: Array[Sprite2D] = []

func setup_terrain(type: String):
	terrain_type = type
	set_terrain_sprite()
	determine_resources()

func setup_terrain_advanced(tile_data: Dictionary):
	terrain_type = tile_data.get("terrain_type", "grass")
	resources = tile_data.get("resources", [])
	fertility = tile_data.get("fertility", 0.5)
	elevation = tile_data.get("elevation", 0.5)
	temperature = tile_data.get("temperature", 0.5)
	humidity = tile_data.get("humidity", 0.5)
	vegetation = tile_data.get("vegetation", [])
	
	set_terrain_sprite()
	setup_vegetation()

func set_terrain_sprite():
	var sprite_path = "res://sprites/terrain/%s.png" % terrain_type
	var terrain_texture = load(sprite_path)
	if terrain_texture:
		texture = terrain_texture
	else:
		# Fallback to grass if texture not found
		texture = load("res://sprites/terrain/grass.png")

func setup_vegetation():
	# Clear existing vegetation
	for veg_sprite in vegetation_sprites:
		veg_sprite.queue_free()
	vegetation_sprites.clear()
	
	# Add vegetation sprites
	for veg_type in vegetation:
		var veg_sprite = Sprite2D.new()
		var veg_path = "res://sprites/vegetation/%s.png" % veg_type
		var veg_texture = load(veg_path)
		
		if veg_texture:
			veg_sprite.texture = veg_texture
			veg_sprite.position = Vector2(randf_range(-8, 8), randf_range(-8, 8))
			veg_sprite.scale = Vector2(0.8, 0.8)
			add_child(veg_sprite)
			vegetation_sprites.append(veg_sprite)

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

func get_tile_info() -> Dictionary:
	return {
		"terrain_type": terrain_type,
		"resources": resources,
		"fertility": fertility,
		"elevation": elevation,
		"temperature": temperature,
		"humidity": humidity,
		"vegetation": vegetation
	}

func _ready():
	# Add tooltip functionality - TerrainTile extends Sprite2D which doesn't have mouse signals
	# We'll handle this in the scene instead if needed
	pass

# Mouse interaction functions - these would need to be connected manually if needed
func _on_mouse_entered():
	modulate = Color(1.2, 1.2, 1.2)

func _on_mouse_exited():
	modulate = Color.WHITE