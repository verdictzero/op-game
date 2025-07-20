# 🌍 Cosmic Civilization - Procedural World Generation Demo

## Overview
A complete working demo showcasing advanced procedural world generation with fire spread mechanics, built in Godot 4.4. The demo features realistic terrain generation, climate simulation, and interactive god powers.

## 🚀 Quick Start
1. Open `oneiric-parallax/project.godot` in Godot 4.4+
2. Run the project (F5)
3. Click "NEW WORLD" to start world generation
4. Adjust parameters or choose presets
5. Click "GENERATE WORLD" and watch the progress
6. Review world statistics
7. Click "START GAME" to enter the interactive world

## 🎮 Controls
- **Main Menu**: Navigate with mouse clicks
- **World Generation**: Adjust sliders and dropdowns
- **In-Game**: 
  - WASD: Move camera
  - Mouse Wheel: Zoom in/out
  - Left Click: Start fire at cursor location
  - Right Click: Spawn civilization units
  - ESC: Return to main menu

## 🌟 Key Features

### Procedural World Generation
- **Multi-layered noise generation** for elevation, temperature, and humidity
- **Realistic biome distribution** based on climate factors
- **River generation** following natural elevation gradients
- **Resource placement** based on terrain characteristics
- **Vegetation system** with growth stages and seasonal states

### Advanced Climate Simulation
- **Temperature zones** affected by latitude and elevation
- **Humidity patterns** creating realistic biome transitions
- **Elevation mapping** with mountain ranges and valleys
- **8 distinct terrain types**: grass, forest, desert, water, mountain, snow, swamp, volcanic

### Fire Spread System
- **5 fire intensity levels**: ignition → small → medium → large → dying
- **Realistic spread mechanics** based on terrain flammability
- **34 animated fire sprites** with flames, smoke, and embers
- **Environmental interaction** with vegetation and terrain

### Interactive God Powers
- **Fire starting**: Click to ignite fires that spread naturally
- **Civilization spawning**: Right-click to place primitive units
- **Real-time world manipulation** with immediate visual feedback

### User Interface
- **Main Menu** with clean navigation
- **World Generation Screen** with parameter controls:
  - World size (64x64 to 256x256)
  - Seed input with random generation
  - Climate parameters (temperature, humidity, elevation scales)
  - Resource and vegetation density controls
  - River count settings
  - Preset world types (Earth-like, Desert, Ocean, etc.)
- **In-Game UI** showing:
  - Active fire count
  - God power instructions
  - World statistics
  - Controls help

## 📊 Technical Specifications

### World Generation
- **World sizes**: 64x64 to 256x256 tiles
- **Tile resolution**: 32x32 pixels each
- **Generation phases**: 8 distinct steps with progress tracking
- **Async processing**: Non-blocking generation with frame-rate preservation

### Sprite System
- **137 total sprites** across all categories
- **7 civilization eras**: primitive, ancient, medieval, renaissance, industrial, modern, space
- **Vegetation lifecycle**: 31 sprites covering growth, decay, and seasonal changes
- **Fire animation**: 34 sprites for realistic fire behavior
- **Terrain variety**: 8 base terrain types with variations

### Performance
- **Efficient tile rendering** with sprite batching
- **Smart fire propagation** with distance-based spreading
- **Memory-conscious generation** with garbage collection friendly code
- **Scalable architecture** supporting larger worlds

## 🎯 Preset World Types

1. **Earth-like**: Balanced climate with varied biomes
2. **Desert World**: Arid climate with minimal vegetation
3. **Ocean World**: High humidity with many water bodies
4. **Mountain World**: High elevation variance with peaks and valleys
5. **Forest World**: Dense vegetation coverage
6. **Volcanic World**: High temperature with volcanic terrain

## 🔧 Technical Architecture

### Core Systems
- **WorldGenerator**: Handles all terrain and feature generation
- **FireSystemSimple**: Manages fire lifecycle and spreading
- **GameManager**: Coordinates UI states and game flow
- **TerrainTile**: Individual tile management with data storage

### Data Flow
1. User configures parameters in WorldGenUI
2. WorldGenerator creates noise maps and terrain data
3. TerrainTiles are instantiated with complete environmental data
4. FireSystem monitors flammable areas for spreading
5. GameUI provides real-time feedback and statistics

## 🌱 Expandability
The demo provides a solid foundation for:
- **Civilization AI**: Units already have basic needs and personality systems
- **Technology progression**: Era advancement mechanics are prepared
- **Resource management**: Mining, farming, and trade systems
- **Multiplayer support**: Modular architecture supports networking
- **Custom scenarios**: Easy preset creation and world templates

## 📁 Project Structure
```
oneiric-parallax/
├── scenes/
│   ├── GameManager.tscn          # Main scene
│   ├── ui/                       # User interface screens
│   ├── entities/                 # Game objects (units, buildings)
│   └── world/                    # World tile components
├── scripts/
│   ├── GameManager.gd            # Main game controller
│   ├── systems/                  # Core game systems
│   ├── ui/                       # UI controllers
│   ├── entities/                 # Game object scripts
│   └── world/                    # World generation logic
├── sprites/                      # 137 generated sprites
│   ├── terrain/                  # 8 terrain types
│   ├── vegetation/               # 31 vegetation sprites
│   ├── fire/                     # 34 fire animation frames
│   └── [eras]/                   # 7 civilization eras
└── project.godot                 # Godot project configuration
```

## 🎊 Demo Highlights
- **Complete gameplay loop**: From world generation to interactive play
- **Visual progression**: Watch worlds come alive through generation phases
- **Emergent gameplay**: Fire spreads create dynamic scenarios
- **Educational value**: Demonstrates advanced procedural generation techniques
- **Professional quality**: Production-ready code with proper architecture

---

*Built with Godot 4.4 • Procedural generation • Fire simulation • Interactive world building*