# Pixel Art Visual Design System
*WorldBox-inspired visuals for cosmic scale*

## Art Direction

### Core Visual Principles
- **Readable Simplicity**: Every element instantly recognizable
- **Consistent Scale**: Maintain pixel ratios across zoom levels
- **Living Motion**: Constant small animations bring life
- **Clear Progression**: Visual evolution shows advancement
- **Delightful Details**: Small touches that reward observation

## Sprite Specifications

### Character Sprites (Planetary View)

#### Primitive Era (8x8 pixels)
```
BASIC HUMANOID
  ▓▓    <- Head (skin tone)
 ▓██▓   <- Body (clothing color)
  ▓▓    <- Legs
  
VARIATIONS:
- Skin tones: 6 options
- Clothing: Indicates role (hunter, farmer, leader)
- Tools: +2 pixels for spears, hoes, etc.
- Animation: 2-frame walk cycle
```

#### Advanced Era (8x8 pixels, more detail)
```
INDUSTRIAL CITIZEN
  ▓▓    <- Hat/Hair
 ▓▓▓▓   <- More detailed clothing
  ██    <- Pants
  
VARIATIONS:
- Outfits: Worker, soldier, scientist, leader
- Items: Briefcases, weapons, tools
- Vehicles: +4x4 pixel cars, trains
```

#### Space Era (8x8 base + equipment)
```
SPACE COLONIST
  ◊◊    <- Helmet
 ◊◊◊◊   <- Space suit
  ◊◊    <- Boots
  
VARIATIONS:
- Suit colors by civilization
- Jetpack variants
- Alien species modifications
```

### Building Sprites

#### Primitive Buildings (16x16 pixels)
```
HUT                 FARM
   ╱▔▔╲              ████  <- Roof
  ╱────╲             █┌┐█  <- Walls
 │ ┌┐  │             └┘└┘  <- Door
 └─┴┴──┘             ~~~~ <- Crops

TEMPLE              WORKSHOP
  ▲▲▲▲               ╔══╗
 ╔════╗              ║██║ <- Smoke
 ║╬╬╬╬║              ║▓▓║
 ╚════╝              ╚══╝
```

#### Advanced Buildings (16x16 to 32x32)
```
FACTORY (24x24)          SKYSCRAPER (16x32)
 ┌─┬─┬─┐                    ╔═╗
 │█│█│█│ <- Smokestacks     ║▓║
 ├─┼─┼─┤                    ║▓║
 │▓│▓│▓│                    ║▓║
 └─┴─┴─┘                    ║▓║
                            ╚═╝

NUCLEAR PLANT           SPACE PORT
   ◊◊◊◊                 ╱───╲
  ╱    ╲                │ ▲ │
 │  ◊◊  │               │ │ │
 └──────┘               └───┘
```

#### Megastructures (48x48 to 128x128)
```
DYSON PANEL (32x32)     ORBITAL RING (64x64)
 ╔═══════╗              ╭─────────╮
 ║▓▓▓▓▓▓▓║              │ ╭─────╮ │
 ║▓▓▓▓▓▓▓║              │ │     │ │
 ║▓▓▓▓▓▓▓║              │ ╰─────╯ │
 ╚═══════╝              ╰─────────╯
```

### Terrain Tiles (8x8 base, tileable)

#### Biomes
```
GRASS    DESERT   SNOW     WATER
████     ▒▒▒▒     ░░░░     ≈≈≈≈
████     ▒▒▒▒     ░░░░     ≈≈≈≈

FOREST   MOUNTAIN SWAMP    VOLCANIC
▲▲▲▲     ╱╲╱╲    ≈██≈     ▓◊▓◊
████     ████     ████     ████
```

### Effects and Particles

#### Combat Effects
```
EXPLOSION (16x16, 4 frames)
Frame 1: ✦
Frame 2: ✦✦✦
Frame 3: ◊◊◊◊◊
Frame 4: . . .

LASER (pixel line)
━━━━━► (color varies by tech level)
```

#### Environmental Effects
```
RAIN     SNOW     METEOR   RADIATION
│││││    ❅ ❅ ❅   ☄️       ░░░░░
│││││    ❅ ❅ ❅            ░░░░░
```

## Zoom Level Adaptations

### Planet View (1:1 pixel)
- All individual units visible
- Buildings show full detail
- Terrain tiles at maximum detail
- Weather effects visible

### Continental View (1:4 reduction)
- Units become single pixels
- Buildings become color blocks
- Cities show as clusters
- Major terrain features visible

### Space View (1:16 reduction)
- Planets as circles with visible biomes
- Ships as moving dots
- Stations as small icons
- Asteroid belts as particle clouds

### Galactic View (Abstract)
- Star systems as glowing points
- Civilization territories as colored regions
- Trade routes as flowing lines
- Cosmic phenomena as effects

## Animation System

### Idle Animations
- Characters: Breathing, looking around (2-3 frames)
- Buildings: Smoke, lights flickering
- Water: Wave motion (4 frames)
- Trees: Gentle sway (2 frames)

### Action Animations
- Walking: 2-frame cycle
- Combat: 3-frame attack sequence
- Building: 4-frame construction
- Death: 2-frame fall

### Continuous Effects
- Smoke: Rising particles
- Fire: 3-frame flicker
- Energy shields: Pulsing outline
- Portals: Swirling effect

## Color Palettes

### Era-Based Palettes
```
PRIMITIVE ERA
- Earth tones: Browns, greens, grays
- Natural materials: Wood, stone, hide
- Limited metals: Bronze, iron

INDUSTRIAL ERA
- Grays and blacks: Concrete, steel
- Pollution: Browns, dark greens
- Bright accents: Neon signs, lights

SPACE ERA
- Metallics: Silver, chrome, gold
- Energy colors: Cyan, purple, bright green
- Dark space: Deep blues and blacks

TRANSCENDENT ERA
- Ethereal: Translucent whites, pastels
- Energy beings: Bright, shifting colors
- Reality distortion: Inverted colors
```

### Civilization Colors
- 16 distinct color schemes
- Each includes primary, secondary, and accent
- Applied to units, buildings, and territories
- Glow effects for advanced civilizations

## UI Elements

### HUD Elements (Pixel Perfect)
```
RESOURCE ICONS (8x8)
Food: 🍞  Wood: 🪵  Stone: ⛏️  Metal: ⚙️
Energy: ⚡ Science: 🧪 Faith: ✨ Exotic: ◊

TOOL ICONS (16x16)
Life Seed: 🌱    Meteor: ☄️     Inspire: 💡
Disaster: 🌋    Blessing: ✨   Time: ⏰
```

### Menus and Panels
- Pixel font (5x7 characters)
- 9-slice borders for scalable panels
- Simple button states (normal, hover, pressed)
- Tooltip boxes with rounded corners

## Special Effects

### Civilization Advancement
- Particle burst when discovering technology
- Building transformation animations
- Territory border shimmer on expansion
- Achievement star burst effects

### Cosmic Events
- Supernova: Expanding ring of pixels
- Black hole: Swirling pixel distortion
- Wormhole: Portal effect with particles
- Reality tear: Glitch-style corruption

### Transcendence Effects
- Civilization pixels gradually become translucent
- Energy trail effects for ascending beings
- Reality distortion around transcendent entities
- Dimensional rift opening animations

## Performance Considerations

### Sprite Batching
- All similar sprites drawn in single draw call
- Texture atlases for each era/type
- Instanced rendering for large populations

### LOD System
- Distant objects use simplified sprites
- Animation frequency reduces with distance
- Particle effects culled when zoomed out

### Memory Optimization
- Shared sprite sheets per era
- Palette swapping for variations
- Procedural details for large structures

## Art Production Pipeline

### Asset Creation
1. Design in 1x resolution
2. Test readability at multiple zoom levels
3. Create variations for different eras/types
4. Optimize for texture atlas packing

### Animation Guidelines
1. Minimum frames for smooth motion
2. Loop points for continuous animations
3. State transition frames when needed
4. Export as sprite sheets

### Quality Standards
- No anti-aliasing (pure pixel art)
- Consistent pixel sizing
- Clear silhouettes
- Distinct civilization identities

This visual system ensures the game maintains WorldBox's charming and readable aesthetic while scaling up to cosmic proportions. Every element is designed to be instantly recognizable and delightful to watch, whether observing a single farmer or an entire galactic civilization.