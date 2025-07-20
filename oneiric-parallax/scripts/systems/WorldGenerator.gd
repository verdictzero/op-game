extends Node
class_name WorldGenerator

signal generation_progress(progress: float, message: String)
signal generation_complete()

var terrain_tiles: Array[TerrainTile]
var world_size: Vector2i = Vector2i(64, 64)  # Smaller world for faster generation
var tile_size: int = 32

# World generation parameters
var seed_value: int = 0
var temperature_scale: float = 0.1
var humidity_scale: float = 0.15
var elevation_scale: float = 0.08
var resource_density: float = 0.3
var vegetation_density: float = 0.4
var river_count: int = 3

# Noise generators
var elevation_noise: FastNoiseLite
var temperature_noise: FastNoiseLite
var humidity_noise: FastNoiseLite
var resource_noise: FastNoiseLite

# World data
var world_data: Array[Array] = []

func _ready():
	setup_noise_generators()

func setup_noise_generators():
	elevation_noise = FastNoiseLite.new()
	temperature_noise = FastNoiseLite.new()
	humidity_noise = FastNoiseLite.new()
	resource_noise = FastNoiseLite.new()
	
	# Configure noise types
	elevation_noise.noise_type = FastNoiseLite.TYPE_PERLIN
	temperature_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX
	humidity_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX
	resource_noise.noise_type = FastNoiseLite.TYPE_CELLULAR

func set_generation_params(params: Dictionary):
	if params.has("world_size"):
		world_size = params.world_size
	if params.has("seed"):
		seed_value = params.seed
	if params.has("temperature_scale"):
		temperature_scale = params.temperature_scale
	if params.has("humidity_scale"):
		humidity_scale = params.humidity_scale
	if params.has("elevation_scale"):
		elevation_scale = params.elevation_scale
	if params.has("resource_density"):
		resource_density = params.resource_density
	if params.has("vegetation_density"):
		vegetation_density = params.vegetation_density
	if params.has("river_count"):
		river_count = params.river_count
	
	# Update noise seeds
	elevation_noise.seed = seed_value
	temperature_noise.seed = seed_value + 1
	humidity_noise.seed = seed_value + 2
	resource_noise.seed = seed_value + 3
	
	# Update scales
	elevation_noise.frequency = elevation_scale
	temperature_noise.frequency = temperature_scale
	humidity_noise.frequency = humidity_scale
	resource_noise.frequency = 0.2

func generate_world(container: Node2D):
	generate_world_async(container)

func generate_world_async(container: Node2D):
	print("Starting world generation...")
	generation_progress.emit(0.0, "Initializing world data...")
	
	# Clear existing world
	clear_world(container)
	
	# Initialize world data array
	world_data = []
	for x in range(world_size.x):
		world_data.append([])
		for y in range(world_size.y):
			world_data[x].append({})
	
	# Generation phases
	await generate_elevation_map()
	await generate_climate_map()
	await generate_terrain_types()
	await generate_resources()
	await generate_rivers()
	await generate_vegetation()
	await create_world_tiles(container)
	
	generation_progress.emit(1.0, "World generation complete!")
	generation_complete.emit()

func clear_world(container: Node2D):
	terrain_tiles.clear()
	for child in container.get_children():
		child.queue_free()

func generate_elevation_map():
	generation_progress.emit(0.1, "Generating elevation map...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var elevation = elevation_noise.get_noise_2d(x, y)
			# Normalize to 0-1 range
			elevation = (elevation + 1.0) / 2.0
			world_data[x][y]["elevation"] = elevation
		
		# Yield occasionally to prevent frame drops
		if x % 10 == 0:
			await get_tree().process_frame

func generate_climate_map():
	generation_progress.emit(0.2, "Generating climate map...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var temperature = temperature_noise.get_noise_2d(x, y)
			var humidity = humidity_noise.get_noise_2d(x, y)
			
			# Normalize to 0-1 range
			temperature = (temperature + 1.0) / 2.0
			humidity = (humidity + 1.0) / 2.0
			
			# Modify temperature based on elevation (higher = colder)
			var elevation_factor = world_data[x][y]["elevation"]
			temperature -= elevation_factor * 0.3
			
			# Modify temperature based on latitude (poles are colder)
			var latitude_factor = abs(y - world_size.y / 2.0) / (world_size.y / 2.0)
			temperature -= latitude_factor * 0.4
			
			world_data[x][y]["temperature"] = clamp(temperature, 0.0, 1.0)
			world_data[x][y]["humidity"] = clamp(humidity, 0.0, 1.0)
		
		if x % 10 == 0:
			await get_tree().process_frame

func generate_terrain_types():
	generation_progress.emit(0.4, "Determining terrain types...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var elevation = world_data[x][y]["elevation"]
			var temperature = world_data[x][y]["temperature"]
			var humidity = world_data[x][y]["humidity"]
			
			var terrain_type = determine_terrain_type_advanced(elevation, temperature, humidity)
			world_data[x][y]["terrain_type"] = terrain_type
		
		if x % 10 == 0:
			await get_tree().process_frame

func determine_terrain_type_advanced(elevation: float, temperature: float, humidity: float) -> String:
	# Water level
	if elevation < 0.3:
		return "water"
	
	# Mountain level
	if elevation > 0.8:
		if temperature < 0.3:
			return "snow"
		else:
			return "mountain"
	
	# Volcanic areas (high elevation + high temperature)
	if elevation > 0.7 and temperature > 0.8:
		return "volcanic"
	
	# Based on temperature and humidity
	if temperature < 0.2:
		return "snow"
	elif temperature < 0.4:
		if humidity > 0.6:
			return "forest"
		else:
			return "grass"
	elif temperature < 0.7:
		if humidity > 0.7:
			return "forest"
		elif humidity > 0.4:
			return "grass"
		else:
			return "desert"
	else:  # Hot climates
		if humidity > 0.8:
			return "swamp"
		elif humidity > 0.3:
			return "grass"
		else:
			return "desert"

func generate_resources():
	generation_progress.emit(0.6, "Placing resources...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var terrain_type = world_data[x][y]["terrain_type"]
			var elevation = world_data[x][y]["elevation"]
			var resource_value = resource_noise.get_noise_2d(x, y)
			
			var resources = []
			var fertility = randf()
			
			# Resource placement based on terrain and noise
			if resource_value > (1.0 - resource_density):
				match terrain_type:
					"grass":
						resources.append("food")
						fertility *= 1.2
					"forest":
						resources.append("wood")
						if randf() < 0.3:
							resources.append("food")
					"mountain":
						if randf() < 0.6:
							resources.append("stone")
						if randf() < 0.2:
							resources.append("metal")
					"desert":
						if randf() < 0.1:
							resources.append("rare_minerals")
						fertility *= 0.2
					"water":
						resources.append("fish")
					"volcanic":
						if randf() < 0.4:
							resources.append("obsidian")
					"swamp":
						if randf() < 0.3:
							resources.append("peat")
			
			world_data[x][y]["resources"] = resources
			world_data[x][y]["fertility"] = fertility
		
		if x % 10 == 0:
			await get_tree().process_frame

func generate_rivers():
	generation_progress.emit(0.7, "Carving rivers...")
	
	for i in range(river_count):
		generate_river()
		if i % 2 == 0:
			await get_tree().process_frame

func generate_river():
	# Find high elevation starting point
	var start_x = randi() % world_size.x
	var start_y = randi() % world_size.y
	var highest_elevation = 0.0
	
	# Find the highest point in a random area
	for x in range(max(0, start_x - 10), min(world_size.x, start_x + 10)):
		for y in range(max(0, start_y - 10), min(world_size.y, start_y + 10)):
			if world_data[x][y]["elevation"] > highest_elevation:
				highest_elevation = world_data[x][y]["elevation"]
				start_x = x
				start_y = y
	
	# Trace river downhill
	var current_x = start_x
	var current_y = start_y
	var visited = {}
	
	while true:
		var key = str(current_x) + "," + str(current_y)
		if visited.has(key):
			break
		visited[key] = true
		
		# Mark as water if not already water
		if world_data[current_x][current_y]["terrain_type"] != "water":
			world_data[current_x][current_y]["terrain_type"] = "water"
			world_data[current_x][current_y]["resources"] = ["fish"]
		
		# Find steepest descent
		var lowest_elevation = world_data[current_x][current_y]["elevation"]
		var next_x = current_x
		var next_y = current_y
		
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if dx == 0 and dy == 0:
					continue
				var nx = current_x + dx
				var ny = current_y + dy
				
				if nx >= 0 and nx < world_size.x and ny >= 0 and ny < world_size.y:
					if world_data[nx][ny]["elevation"] < lowest_elevation:
						lowest_elevation = world_data[nx][ny]["elevation"]
						next_x = nx
						next_y = ny
		
		# If no lower elevation found, stop
		if next_x == current_x and next_y == current_y:
			break
		
		current_x = next_x
		current_y = next_y
		
		# Stop if we reach water or edge
		if world_data[current_x][current_y]["elevation"] < 0.3:
			break

func generate_vegetation():
	generation_progress.emit(0.8, "Growing vegetation...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var terrain_type = world_data[x][y]["terrain_type"]
			var humidity = world_data[x][y]["humidity"]
			var fertility = world_data[x][y]["fertility"]
			
			var vegetation = []
			
			if randf() < vegetation_density * fertility:
				match terrain_type:
					"grass":
						if randf() < 0.6:
							vegetation.append("grass_healthy")
						if randf() < 0.2:
							vegetation.append("flowers_healthy")
					"forest":
						if randf() < 0.8:
							vegetation.append("tree_mature")
						if randf() < 0.3:
							vegetation.append("bush_healthy")
					"swamp":
						if randf() < 0.4:
							vegetation.append("tree_sapling")
						if randf() < 0.5:
							vegetation.append("grass_dry")
					"desert":
						if randf() < 0.1:
							vegetation.append("bush_dead")
			
			world_data[x][y]["vegetation"] = vegetation
		
		# More frequent yielding and progress updates
		if x % 2 == 0:  # Even more frequent yielding
			var progress = 0.8 + (float(x) / world_size.x) * 0.1
			generation_progress.emit(progress, "Growing vegetation... (%d/%d)" % [x + 1, world_size.x])
			await get_tree().process_frame

func create_world_tiles(container: Node2D):
	generation_progress.emit(0.9, "Creating world tiles...")
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var tile_data = world_data[x][y]
			create_terrain_tile_advanced(x, y, tile_data, container)
		
		# More frequent yielding for large worlds
		if x % 2 == 0:  # Even more frequent yielding
			var progress = 0.9 + (float(x) / world_size.x) * 0.1
			generation_progress.emit(progress, "Creating world tiles... (%d/%d)" % [x + 1, world_size.x])
			await get_tree().process_frame

func create_terrain_tile_advanced(x: int, y: int, tile_data: Dictionary, container: Node2D):
	var tile_scene = preload("res://scenes/world/TerrainTile.tscn")
	var tile = tile_scene.instantiate()
	
	tile.position = Vector2(x * tile_size, y * tile_size)
	tile.setup_terrain_advanced(tile_data)
	
	container.add_child(tile)
	terrain_tiles.append(tile)

func get_world_stats() -> Dictionary:
	var stats = {
		"total_tiles": world_size.x * world_size.y,
		"terrain_counts": {},
		"resource_counts": {},
		"avg_elevation": 0.0,
		"avg_temperature": 0.0,
		"avg_humidity": 0.0
	}
	
	var total_elevation = 0.0
	var total_temperature = 0.0
	var total_humidity = 0.0
	
	for x in range(world_size.x):
		for y in range(world_size.y):
			var tile_data = world_data[x][y]
			
			# Count terrain types
			var terrain = tile_data.get("terrain_type", "unknown")
			if not stats.terrain_counts.has(terrain):
				stats.terrain_counts[terrain] = 0
			stats.terrain_counts[terrain] += 1
			
			# Count resources
			var resources = tile_data.get("resources", [])
			for resource in resources:
				if not stats.resource_counts.has(resource):
					stats.resource_counts[resource] = 0
				stats.resource_counts[resource] += 1
			
			# Sum climate data
			total_elevation += tile_data.get("elevation", 0.0)
			total_temperature += tile_data.get("temperature", 0.0)
			total_humidity += tile_data.get("humidity", 0.0)
	
	# Calculate averages
	var total_tiles = stats.total_tiles
	stats.avg_elevation = total_elevation / total_tiles
	stats.avg_temperature = total_temperature / total_tiles
	stats.avg_humidity = total_humidity / total_tiles
	
	return stats
