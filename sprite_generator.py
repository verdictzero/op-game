#!/usr/bin/env python3
"""
Sprite Generator for Cosmic Civilization Game
Generates placeholder pixel art sprites for different eras and entities
"""

import os
import sys
from PIL import Image, ImageDraw
import json
from pathlib import Path
import math

# Color palettes for different eras
COLOR_PALETTES = {
    "primitive": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(139, 105, 70), (160, 132, 92), (101, 67, 33)],
        "hair": [(101, 67, 33), (139, 105, 70), (64, 64, 64), (32, 32, 32)],
        "tools": [(169, 169, 169), (139, 105, 70)],
        "buildings": [(139, 105, 70), (160, 132, 92), (105, 105, 105)]
    },
    "ancient": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(255, 255, 255), (139, 0, 0), (218, 165, 32), (128, 0, 128)],
        "hair": [(101, 67, 33), (139, 105, 70), (64, 64, 64), (32, 32, 32)],
        "tools": [(205, 133, 63), (192, 192, 192), (218, 165, 32)],
        "buildings": [(245, 245, 220), (205, 133, 63), (128, 128, 128), (218, 165, 32)]
    },
    "medieval": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(128, 128, 128), (139, 0, 0), (0, 0, 139), (34, 139, 34)],
        "hair": [(101, 67, 33), (139, 105, 70), (64, 64, 64), (255, 215, 0)],
        "tools": [(192, 192, 192), (139, 69, 19), (105, 105, 105)],
        "buildings": [(169, 169, 169), (139, 69, 19), (105, 105, 105), (178, 34, 34)]
    },
    "renaissance": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(139, 0, 139), (255, 215, 0), (0, 100, 0), (178, 34, 34)],
        "hair": [(101, 67, 33), (139, 105, 70), (255, 255, 255), (32, 32, 32)],
        "tools": [(218, 165, 32), (192, 192, 192), (139, 69, 19)],
        "buildings": [(255, 228, 196), (178, 34, 34), (245, 245, 220), (139, 69, 19)]
    },
    "industrial": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(64, 64, 64), (32, 32, 32), (139, 0, 0), (0, 0, 139)],
        "hair": [(101, 67, 33), (139, 105, 70), (64, 64, 64), (32, 32, 32)],
        "tools": [(169, 169, 169), (105, 105, 105), (64, 64, 64)],
        "buildings": [(105, 105, 105), (169, 169, 169), (64, 64, 64), (32, 32, 32)]
    },
    "modern": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(70, 130, 180), (255, 255, 255), (64, 64, 64), (255, 165, 0)],
        "hair": [(101, 67, 33), (139, 105, 70), (255, 182, 193), (0, 255, 127)],
        "tools": [(192, 192, 192), (64, 64, 64), (255, 165, 0)],
        "buildings": [(245, 245, 245), (70, 130, 180), (255, 165, 0), (152, 251, 152)]
    },
    "space": {
        "skin": [(222, 184, 135), (160, 132, 92), (139, 105, 70), (94, 65, 47)],
        "clothing": [(240, 248, 255), (169, 169, 169), (0, 191, 255), (255, 215, 0)],
        "hair": [(101, 67, 33), (139, 105, 70), (64, 64, 64), (32, 32, 32)],
        "tools": [(192, 192, 192), (255, 215, 0), (0, 191, 255)],
        "buildings": [(192, 192, 192), (169, 169, 169), (0, 191, 255), (255, 215, 0)]
    }
}

# Terrain colors
TERRAIN_COLORS = {
    "grass": (34, 139, 34),
    "desert": (238, 203, 173),
    "snow": (255, 250, 250),
    "water": (65, 105, 225),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137),
    "swamp": (107, 142, 35),
    "volcanic": (178, 34, 34)
}

# Fire color palettes for different intensities and stages
FIRE_COLORS = {
    "ignition": {
        "core": [(255, 69, 0), (255, 99, 71), (255, 140, 0)],
        "outer": [(255, 165, 0), (255, 215, 0), (255, 255, 0)],
        "sparks": [(255, 255, 255), (255, 255, 224), (255, 215, 0)]
    },
    "small": {
        "core": [(178, 34, 34), (255, 69, 0), (255, 99, 71)],
        "outer": [(255, 140, 0), (255, 165, 0), (255, 215, 0)],
        "sparks": [(255, 215, 0), (255, 255, 0), (255, 255, 255)]
    },
    "medium": {
        "core": [(139, 0, 0), (178, 34, 34), (255, 69, 0)],
        "outer": [(255, 99, 71), (255, 140, 0), (255, 165, 0)],
        "sparks": [(255, 165, 0), (255, 215, 0), (255, 255, 255)]
    },
    "large": {
        "core": [(128, 0, 0), (139, 0, 0), (178, 34, 34)],
        "outer": [(255, 69, 0), (255, 99, 71), (255, 140, 0)],
        "sparks": [(255, 140, 0), (255, 165, 0), (255, 255, 255)]
    },
    "dying": {
        "core": [(105, 105, 105), (128, 128, 128), (169, 169, 169)],
        "outer": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
        "sparks": [(255, 140, 0), (255, 69, 0), (178, 34, 34)]
    },
    "embers": {
        "hot": [(255, 69, 0), (255, 140, 0), (255, 165, 0)],
        "warm": [(255, 165, 0), (255, 215, 0), (255, 255, 0)],
        "cool": [(139, 69, 19), (160, 82, 45), (128, 128, 128)]
    },
    "smoke": {
        "thick": [(64, 64, 64), (96, 96, 96), (128, 128, 128)],
        "light": [(169, 169, 169), (192, 192, 192), (211, 211, 211)],
        "wispy": [(211, 211, 211), (220, 220, 220), (245, 245, 245)]
    }
}

# Vegetation color palettes for different stages and states
VEGETATION_COLORS = {
    "tree": {
        "healthy": {
            "trunk": [(101, 67, 33), (139, 69, 19), (160, 82, 45)],
            "foliage": [(34, 139, 34), (0, 128, 0), (50, 205, 50), (144, 238, 144)]
        },
        "autumn": {
            "trunk": [(101, 67, 33), (139, 69, 19)],
            "foliage": [(255, 165, 0), (255, 140, 0), (178, 34, 34), (255, 215, 0)]
        },
        "dead": {
            "trunk": [(69, 69, 69), (105, 105, 105), (128, 128, 128)],
            "foliage": [(139, 69, 19), (160, 82, 45), (205, 133, 63)]
        },
        "burnt": {
            "trunk": [(32, 32, 32), (64, 64, 64), (96, 96, 96)],
            "foliage": [(0, 0, 0), (32, 32, 32), (64, 64, 64)]
        }
    },
    "crops": {
        "wheat": {
            "seed": [(139, 69, 19), (160, 82, 45)],
            "sprout": [(34, 139, 34), (50, 205, 50)],
            "growing": [(34, 139, 34), (0, 128, 0)],
            "mature": [(255, 215, 0), (218, 165, 32), (184, 134, 11)],
            "dead": [(139, 69, 19), (160, 82, 45), (205, 133, 63)]
        },
        "corn": {
            "seed": [(139, 69, 19), (160, 82, 45)],
            "sprout": [(34, 139, 34), (50, 205, 50)],
            "growing": [(34, 139, 34), (0, 128, 0)],
            "mature": [(255, 215, 0), (34, 139, 34), (218, 165, 32)],
            "dead": [(139, 69, 19), (160, 82, 45)]
        },
        "vegetables": {
            "seed": [(139, 69, 19), (160, 82, 45)],
            "sprout": [(50, 205, 50), (144, 238, 144)],
            "growing": [(34, 139, 34), (0, 128, 0)],
            "mature": [(34, 139, 34), (255, 99, 71), (255, 165, 0)],
            "dead": [(139, 69, 19), (105, 105, 105)]
        }
    },
    "grass": {
        "healthy": [(34, 139, 34), (50, 205, 50), (144, 238, 144)],
        "dry": [(255, 215, 0), (218, 165, 32), (184, 134, 11)],
        "dead": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
        "burnt": [(32, 32, 32), (64, 64, 64)]
    },
    "flowers": {
        "healthy": [(255, 20, 147), (255, 105, 180), (255, 192, 203), (34, 139, 34)],
        "wilted": [(139, 69, 19), (160, 82, 45), (105, 105, 105)],
        "dead": [(69, 69, 69), (105, 105, 105)]
    }
}

class SpriteGenerator:
    def __init__(self, output_dir="oneiric-parallax/sprites"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for era in ["primitive", "ancient", "medieval", "renaissance", "industrial", "modern", "space"]:
            (self.output_dir / era).mkdir(exist_ok=True)
        
        (self.output_dir / "terrain").mkdir(exist_ok=True)
        (self.output_dir / "effects").mkdir(exist_ok=True)
        (self.output_dir / "vegetation").mkdir(exist_ok=True)
        (self.output_dir / "fire").mkdir(exist_ok=True)
        
    def create_image(self, width, height, scale=1):
        """Create a new image with proper scaling"""
        return Image.new('RGBA', (width * scale, height * scale), (0, 0, 0, 0))
    
    def draw_pixel(self, draw, x, y, color, scale=1):
        """Draw a scaled pixel"""
        if scale == 1:
            draw.point((x, y), color)
        else:
            draw.rectangle([x*scale, y*scale, (x+1)*scale-1, (y+1)*scale-1], fill=color)
    
    def generate_unit_sprite(self, era, unit_type, scale=2):
        """Generate a unit sprite for the given era and type"""
        img = self.create_image(32, 32, scale)
        draw = ImageDraw.Draw(img)
        palette = COLOR_PALETTES[era]
        
        # Draw basic humanoid first
        self.draw_basic_humanoid(draw, palette, scale)
        
        # Add variations based on unit type
        if unit_type == "leader":
            # Add elaborate gold crown
            gold_color = (255, 215, 0)  # Gold
            crown_jewel = (255, 0, 0)   # Red jewel
            
            # Crown base
            for x in range(12, 20):
                for y in range(1, 4):
                    self.draw_pixel(draw, x, y, gold_color, scale)
            
            # Crown spikes/points
            crown_points = [(13, 0), (16, 0), (19, 0)]
            for px, py in crown_points:
                self.draw_pixel(draw, px, py, gold_color, scale)
                self.draw_pixel(draw, px, py - 1, gold_color, scale)
            
            # Central jewel
            self.draw_pixel(draw, 16, 2, crown_jewel, scale)
            
            # Royal cape
            cape_color = (139, 0, 139)  # Purple
            for x in range(8, 24):
                for y in range(12, 26):
                    if x < 10 or x > 21:  # Cape sides
                        dist_from_center = abs(x - 16)
                        if y - 12 < 26 - y - dist_from_center:
                            self.draw_pixel(draw, x, y, cape_color, scale)
            
        elif unit_type == "warrior":
            # Add large weapon (sword/spear)
            weapon_color = palette["tools"][0]
            # Sword/spear shaft
            for y in range(4, 24):
                self.draw_pixel(draw, 4, y, weapon_color, scale)
                self.draw_pixel(draw, 5, y, weapon_color, scale)
            # Sword blade/spear tip
            for y in range(0, 5):
                self.draw_pixel(draw, 4, y, tuple(min(255, c + 50) for c in weapon_color), scale)
                self.draw_pixel(draw, 5, y, tuple(min(255, c + 50) for c in weapon_color), scale)
            
            # Add armor details (darker/metallic clothing)
            armor_color = tuple(max(0, c - 30) for c in palette["clothing"][0])
            # Chest plate
            for x in range(10, 22):
                for y in range(11, 18):
                    self.draw_pixel(draw, x, y, armor_color, scale)
            
            # Shoulder guards
            for x in range(8, 11):
                for y in range(11, 14):
                    self.draw_pixel(draw, x, y, armor_color, scale)
            for x in range(21, 24):
                for y in range(11, 14):
                    self.draw_pixel(draw, x, y, armor_color, scale)
            
            # Helmet
            helmet_color = (120, 120, 120)
            for x in range(12, 20):
                for y in range(2, 6):
                    if ((x - 16) ** 2 + (y - 5) ** 2) ** 0.5 <= 4.5:
                        self.draw_pixel(draw, x, y, helmet_color, scale)
                        
        elif unit_type == "worker":
            # Add large tool (hammer/pickaxe)
            tool_handle = palette["tools"][0]
            tool_head = palette["tools"][1] if len(palette["tools"]) > 1 else palette["tools"][0]
            
            # Tool handle
            for x in range(24, 28):
                for y in range(12, 22):
                    self.draw_pixel(draw, x, y, tool_handle, scale)
            
            # Tool head (hammer/pick)
            for x in range(23, 30):
                for y in range(8, 13):
                    self.draw_pixel(draw, x, y, tool_head, scale)
            
            # Work apron/vest
            apron_color = (139, 90, 43)  # Brown
            for x in range(11, 21):
                for y in range(16, 24):
                    self.draw_pixel(draw, x, y, apron_color, scale)
            
            # Tool belt
            belt_color = (80, 80, 80)
            for x in range(10, 22):
                for y in range(19, 21):
                    self.draw_pixel(draw, x, y, belt_color, scale)
        
        return img
    
    def draw_basic_humanoid(self, draw, palette, scale):
        """Draw a detailed humanoid figure for 32x32 canvas"""
        # Head (larger and more detailed)
        for x in range(12, 20):
            for y in range(4, 12):
                if ((x - 16) ** 2 + (y - 8) ** 2) ** 0.5 <= 4:
                    self.draw_pixel(draw, x, y, palette["skin"][0], scale)
        
        # Hair
        hair_color = palette["hair"][0]
        for x in range(12, 20):
            for y in range(2, 8):
                if ((x - 16) ** 2 + (y - 5) ** 2) ** 0.5 <= 4.5 and y < 7:
                    self.draw_pixel(draw, x, y, hair_color, scale)
        
        # Eyes
        self.draw_pixel(draw, 14, 8, (0, 0, 0), scale)
        self.draw_pixel(draw, 18, 8, (0, 0, 0), scale)
        
        # Body/Torso
        for x in range(10, 22):
            for y in range(11, 20):
                self.draw_pixel(draw, x, y, palette["clothing"][0], scale)
        
        # Arms
        # Left arm
        for x in range(6, 11):
            for y in range(12, 22):
                arm_width = 2 if y < 16 else 3
                if x >= 10 - arm_width:
                    if y < 18:
                        self.draw_pixel(draw, x, y, palette["clothing"][0], scale)
                    else:
                        self.draw_pixel(draw, x, y, palette["skin"][0], scale)
        
        # Right arm
        for x in range(21, 26):
            for y in range(12, 22):
                arm_width = 2 if y < 16 else 3
                if x <= 21 + arm_width:
                    if y < 18:
                        self.draw_pixel(draw, x, y, palette["clothing"][0], scale)
                    else:
                        self.draw_pixel(draw, x, y, palette["skin"][0], scale)
        
        # Legs
        leg_color = palette["clothing"][1] if len(palette["clothing"]) > 1 else palette["clothing"][0]
        # Left leg
        for x in range(11, 16):
            for y in range(19, 28):
                self.draw_pixel(draw, x, y, leg_color, scale)
        
        # Right leg
        for x in range(16, 21):
            for y in range(19, 28):
                self.draw_pixel(draw, x, y, leg_color, scale)
        
        # Feet/Shoes
        foot_color = palette["clothing"][2] if len(palette["clothing"]) > 2 else palette["clothing"][0]
        for x in range(10, 16):
            for y in range(27, 30):
                self.draw_pixel(draw, x, y, foot_color, scale)
        for x in range(16, 22):
            for y in range(27, 30):
                self.draw_pixel(draw, x, y, foot_color, scale)
    
    def generate_building_sprite(self, era, building_type, size=64, scale=1):
        """Generate a building sprite"""
        img = self.create_image(size, size, scale)
        draw = ImageDraw.Draw(img)
        palette = COLOR_PALETTES[era]
        
        if building_type in ["hut", "tent", "shrine"]:
            self.draw_primitive_building(draw, building_type, palette, scale)
        elif building_type in ["villa", "temple", "forum"]:
            self.draw_ancient_building(draw, building_type, palette, scale)
        elif building_type in ["castle", "cathedral", "blacksmith"]:
            self.draw_medieval_building(draw, building_type, palette, scale)
        elif building_type in ["mansion", "university", "workshop"]:
            self.draw_renaissance_building(draw, building_type, palette, scale)
        elif building_type in ["house", "factory", "office"]:
            self.draw_industrial_building(draw, building_type, palette, scale)
        elif building_type in ["apartment", "mall", "hospital"]:
            self.draw_modern_building(draw, building_type, palette, scale)
        elif building_type in ["dome", "station", "lab", "factory", "habitat", "solar_array"]:
            self.draw_space_building(draw, building_type, palette, scale)
        
        return img
    
    def draw_primitive_building(self, draw, building_type, palette, scale):
        """Draw primitive era buildings with 64x64 detail"""
        if building_type == "hut":
            # Enhanced tribal hut with thatch roof and wooden details
            thatch_color = palette["buildings"][0]
            thatch_dark = tuple(max(0, c - 30) for c in thatch_color)
            wall_color = palette["buildings"][1]
            wood_color = (101, 67, 33)
            door_color = (80, 53, 26)
            
            # Triangular thatched roof with detailed layers
            roof_peak = 8
            roof_base = 28
            for y in range(roof_peak, roof_base + 1):
                roof_width = (y - roof_peak + 1) * 2
                start_x = 32 - roof_width // 2
                for x in range(start_x, start_x + roof_width):
                    if x >= 8 and x < 56:
                        # Thatch texture with alternating dark/light
                        if (x + y) % 3 == 0:
                            self.draw_pixel(draw, x, y, thatch_dark, scale)
                        else:
                            self.draw_pixel(draw, x, y, thatch_color, scale)
            
            # Roof edge details (hanging thatch)
            for x in range(10, 54, 4):
                for y in range(roof_base + 1, roof_base + 4):
                    if y < 64:
                        self.draw_pixel(draw, x, y, thatch_dark, scale)
            
            # Stone foundation
            foundation_color = (120, 120, 120)
            for x in range(12, 52):
                for y in range(52, 58):
                    if y < 64:
                        self.draw_pixel(draw, x, y, foundation_color, scale)
            
            # Mud brick walls with texture
            for x in range(14, 50):
                for y in range(30, 52):
                    # Brick pattern
                    if (x // 4 + y // 3) % 2 == 0:
                        self.draw_pixel(draw, x, y, wall_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 15) for c in wall_color), scale)
            
            # Wooden door frame and door
            for x in range(26, 38):
                for y in range(40, 52):
                    if x == 26 or x == 37:  # Door frame
                        self.draw_pixel(draw, x, y, wood_color, scale)
                    elif y == 40:  # Top frame
                        self.draw_pixel(draw, x, y, wood_color, scale)
                    else:  # Door itself
                        self.draw_pixel(draw, x, y, door_color, scale)
            
            # Door handle and hinges
            self.draw_pixel(draw, 35, 46, (150, 150, 150), scale)  # Handle
            self.draw_pixel(draw, 27, 42, (80, 80, 80), scale)     # Top hinge
            self.draw_pixel(draw, 27, 48, (80, 80, 80), scale)     # Bottom hinge
            
            # Windows with shutters
            for window_x in [18, 44]:
                # Window frame
                for x in range(window_x, window_x + 6):
                    for y in range(35, 42):
                        if x == window_x or x == window_x + 5 or y == 35 or y == 41:
                            self.draw_pixel(draw, x, y, wood_color, scale)
                        else:
                            self.draw_pixel(draw, x, y, (40, 40, 40), scale)  # Dark interior
                
                # Shutters (partially open)
                for y in range(36, 41):
                    self.draw_pixel(draw, window_x - 1, y, wood_color, scale)
                    self.draw_pixel(draw, window_x + 6, y, wood_color, scale)
            
            # Support beams
            for beam_x in [20, 32, 44]:
                for y in range(28, 32):
                    self.draw_pixel(draw, beam_x, y, wood_color, scale)
                
        elif building_type == "tent":
            # Detailed nomadic tent with rope work and fabric patterns
            tent_color = palette["buildings"][0]
            tent_dark = tuple(max(0, c - 25) for c in tent_color)
            tent_light = tuple(min(255, c + 20) for c in tent_color)
            rope_color = (139, 105, 70)
            stake_color = (101, 67, 33)
            
            # Main tent body with fabric texture
            tent_base_y = 48
            tent_peak_y = 12
            tent_center_x = 32
            
            for y in range(tent_peak_y, tent_base_y + 1):
                width = (y - tent_peak_y + 1) * 2
                start_x = tent_center_x - width // 2
                for x in range(start_x, start_x + width):
                    if x >= 6 and x < 58:
                        # Fabric pattern with seams
                        if (x - start_x) % 8 == 0:  # Vertical seams
                            self.draw_pixel(draw, x, y, tent_dark, scale)
                        elif (y - tent_peak_y) % 6 == 0:  # Horizontal fabric lines
                            self.draw_pixel(draw, x, y, tent_light, scale)
                        else:
                            self.draw_pixel(draw, x, y, tent_color, scale)
            
            # Tent entrance flap (partially open)
            flap_peak_y = 18
            flap_base_y = 44
            for y in range(flap_peak_y, flap_base_y + 1):
                flap_width = (y - flap_peak_y + 1)
                start_x = tent_center_x - flap_width // 2
                for x in range(start_x, start_x + flap_width):
                    if x >= 24 and x <= 40:
                        self.draw_pixel(draw, x, y, tent_dark, scale)
            
            # Tent poles (visible through fabric)
            pole_color = (120, 90, 60)
            for pole_y in range(15, 45):
                self.draw_pixel(draw, 32, pole_y, pole_color, scale)  # Central pole
            
            # Support ropes and guy lines
            rope_points = [(10, 20, 4, 50), (54, 20, 60, 50), (20, 15, 8, 52), (44, 15, 56, 52)]
            for x1, y1, x2, y2 in rope_points:
                # Simple line drawing for ropes
                steps = max(abs(x2 - x1), abs(y2 - y1))
                for i in range(steps + 1):
                    if steps > 0:
                        x = x1 + (x2 - x1) * i // steps
                        y = y1 + (y2 - y1) * i // steps
                        if 0 <= x < 64 and 0 <= y < 64:
                            self.draw_pixel(draw, x, y, rope_color, scale)
            
            # Tent stakes
            stakes = [(4, 50), (60, 50), (8, 52), (56, 52)]
            for stake_x, stake_y in stakes:
                for y in range(stake_y, min(stake_y + 8, 64)):
                    self.draw_pixel(draw, stake_x, y, stake_color, scale)
            
            # Decorative patterns on tent fabric
            pattern_color = tuple(max(0, c - 40) for c in tent_color)
            for pattern_y in range(25, 40, 8):
                for pattern_x in range(16, 48, 12):
                    # Diamond pattern
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            if abs(dx) + abs(dy) == 2:
                                px, py = pattern_x + dx, pattern_y + dy
                                if 6 <= px < 58 and tent_peak_y <= py <= tent_base_y:
                                    self.draw_pixel(draw, px, py, pattern_color, scale)
                        
        elif building_type == "shrine":
            # Detailed ancient temple shrine with ornate decorations
            stone_color = palette["buildings"][2] if len(palette["buildings"]) > 2 else (169, 169, 169)
            marble_color = (220, 220, 220)
            marble_dark = (180, 180, 180)
            gold_color = (255, 215, 0)
            fire_color = (255, 140, 0)
            
            # Multi-level stone platform with steps
            for level, (start_y, end_y) in enumerate([(56, 64), (52, 56), (48, 52)]):
                platform_width = 48 - level * 4
                start_x = 32 - platform_width // 2
                for x in range(start_x, start_x + platform_width):
                    for y in range(start_y, min(end_y, 64)):
                        if (x + y) % 3 == 0:  # Stone texture
                            self.draw_pixel(draw, x, y, tuple(max(0, c - 10) for c in stone_color), scale)
                        else:
                            self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Grand columns (5 columns for more impressive look)
            column_positions = [14, 22, 32, 42, 50]
            for col_x in column_positions:
                # Column shaft with fluting details
                for y in range(20, 45):
                    for x in range(col_x - 2, col_x + 3):
                        if x == col_x - 2 or x == col_x + 2:  # Fluting edges
                            self.draw_pixel(draw, x, y, marble_dark, scale)
                        else:
                            self.draw_pixel(draw, x, y, marble_color, scale)
                
                # Elaborate column capitals (Corinthian style)
                for x in range(col_x - 3, col_x + 4):
                    for y in range(17, 20):
                        self.draw_pixel(draw, x, y, marble_color, scale)
                
                # Capital decorations
                self.draw_pixel(draw, col_x - 2, 16, gold_color, scale)
                self.draw_pixel(draw, col_x + 2, 16, gold_color, scale)
                self.draw_pixel(draw, col_x, 15, gold_color, scale)
                
                # Column base
                for x in range(col_x - 2, col_x + 3):
                    for y in range(45, 48):
                        self.draw_pixel(draw, x, y, marble_dark, scale)
            
            # Pediment (triangular roof) with detailed frieze
            pediment_peak = 8
            pediment_base = 17
            for y in range(pediment_peak, pediment_base):
                width = (y - pediment_peak + 1) * 4
                start_x = 32 - width // 2
                for x in range(start_x, start_x + width):
                    if x >= 10 and x < 54:
                        self.draw_pixel(draw, x, y, marble_color, scale)
            
            # Frieze decorations in pediment
            for frieze_x in range(20, 45, 8):
                for frieze_y in range(12, 15):
                    self.draw_pixel(draw, frieze_x, frieze_y, gold_color, scale)
            
            # Entablature (architrave, frieze, cornice)
            for x in range(12, 52):
                for y in range(16, 18):  # Architrave
                    self.draw_pixel(draw, x, y, marble_color, scale)
                for y in range(14, 16):  # Frieze with gold trim
                    if x % 6 == 0:
                        self.draw_pixel(draw, x, y, gold_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, marble_color, scale)
            
            # Sacred altar in center with elaborate design
            altar_x, altar_y = 32, 35
            for x in range(altar_x - 6, altar_x + 7):
                for y in range(altar_y, altar_y + 8):
                    if x == altar_x - 6 or x == altar_x + 6 or y == altar_y or y == altar_y + 7:
                        self.draw_pixel(draw, x, y, marble_dark, scale)
                    else:
                        self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Sacred fire with flickering animation effect
            fire_positions = [(30, 32), (32, 31), (34, 32), (31, 33), (33, 33)]
            for fx, fy in fire_positions:
                self.draw_pixel(draw, fx, fy, fire_color, scale)
            
            # Golden offerings and decorations
            offering_positions = [(28, 36), (36, 36), (30, 38), (34, 38)]
            for ox, oy in offering_positions:
                self.draw_pixel(draw, ox, oy, gold_color, scale)
            
            # Temple steps leading up to altar
            for step in range(3):
                step_y = 44 + step * 2
                step_width = 20 - step * 2
                start_x = 32 - step_width // 2
                for x in range(start_x, start_x + step_width):
                    for y in range(step_y, step_y + 2):
                        if y < 64:
                            self.draw_pixel(draw, x, y, marble_dark, scale)
    
    def draw_ancient_building(self, draw, building_type, palette, scale):
        """Draw ancient/classical era buildings with 64x64 detail"""
        if building_type == "villa":
            # Roman villa with courtyard
            wall_color = palette["buildings"][0]
            roof_color = palette["buildings"][1]
            column_color = palette["buildings"][2]
            
            # Main villa structure
            for x in range(8, 56):
                for y in range(20, 56):
                    self.draw_pixel(draw, x, y, wall_color, scale)
            
            # Red tile roof
            for y in range(12, 22):
                for x in range(6, 58):
                    if y < 20 - abs(x - 32) // 4:
                        if (x + y) % 3 == 0:
                            self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in roof_color), scale)
                        else:
                            self.draw_pixel(draw, x, y, roof_color, scale)
            
            # Columns at entrance
            for col_x in [16, 24, 40, 48]:
                for y in range(32, 48):
                    for x in range(col_x - 1, col_x + 2):
                        self.draw_pixel(draw, x, y, column_color, scale)
            
            # Central courtyard/atrium
            for x in range(24, 40):
                for y in range(36, 48):
                    if x == 24 or x == 39 or y == 36 or y == 47:
                        self.draw_pixel(draw, x, y, (100, 150, 255), scale)  # Pool edge
                    else:
                        self.draw_pixel(draw, x, y, (65, 105, 225), scale)  # Water
            
            # Mosaic floor pattern
            for x in range(8, 56, 4):
                for y in range(48, 56, 4):
                    self.draw_pixel(draw, x, y, palette["buildings"][3], scale)
            
        elif building_type == "temple":
            # Greek/Roman temple with many columns
            marble_color = palette["buildings"][0]
            gold_color = palette["buildings"][3]
            
            # Platform/steps
            for level in range(3):
                for x in range(10 - level*2, 54 + level*2):
                    for y in range(54 - level*2, 58 - level*2):
                        self.draw_pixel(draw, x, y, marble_color, scale)
            
            # Many columns (Parthenon style)
            for col_x in range(12, 52, 5):
                for y in range(24, 48):
                    for x in range(col_x - 2, col_x + 3):
                        if x == col_x - 2 or x == col_x + 2:
                            self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in marble_color), scale)
                        else:
                            self.draw_pixel(draw, x, y, marble_color, scale)
            
            # Triangular pediment
            for y in range(8, 24):
                width = (y - 8) * 3
                for x in range(32 - width // 2, 32 + width // 2):
                    if x >= 8 and x < 56:
                        self.draw_pixel(draw, x, y, marble_color, scale)
            
            # Frieze with gold details
            for x in range(10, 54):
                for y in range(20, 24):
                    if x % 8 < 3:
                        self.draw_pixel(draw, x, y, gold_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, marble_color, scale)
            
        elif building_type == "forum":
            # Public forum/marketplace
            stone_color = palette["buildings"][2]
            
            # Paved ground
            for x in range(4, 60):
                for y in range(40, 60):
                    if (x // 4 + y // 4) % 2 == 0:
                        self.draw_pixel(draw, x, y, stone_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in stone_color), scale)
            
            # Market stalls
            stall_positions = [(8, 32), (24, 32), (40, 32), (56, 32)]
            for sx, sy in stall_positions:
                if sx < 56:
                    # Stall structure
                    for x in range(sx - 4, min(sx + 4, 64)):
                        for y in range(sy, sy + 8):
                            if y == sy:  # Canopy
                                self.draw_pixel(draw, x, y, (178, 34, 34), scale)
                            else:  # Counter
                                if x == sx - 4 or x == sx + 3:
                                    self.draw_pixel(draw, x, y, (139, 69, 19), scale)
            
            # Central fountain
            for x in range(28, 36):
                for y in range(24, 32):
                    if ((x - 32) ** 2 + (y - 28) ** 2) ** 0.5 <= 4:
                        if ((x - 32) ** 2 + (y - 28) ** 2) ** 0.5 > 3:
                            self.draw_pixel(draw, x, y, stone_color, scale)
                        else:
                            self.draw_pixel(draw, x, y, (100, 150, 255), scale)
            
            # Water spout
            self.draw_pixel(draw, 32, 26, (200, 200, 255), scale)
            self.draw_pixel(draw, 32, 25, (200, 200, 255), scale)

    def draw_medieval_building(self, draw, building_type, palette, scale):
        """Draw medieval era buildings with 64x64 detail"""
        if building_type == "castle":
            # Medieval castle with towers
            stone_color = palette["buildings"][0]
            
            # Main keep
            for x in range(16, 48):
                for y in range(20, 52):
                    # Stone texture
                    if (x // 3 + y // 2) % 3 == 0:
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in stone_color), scale)
                    else:
                        self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Towers
            tower_positions = [(8, 16), (56, 16), (8, 48), (56, 48)]
            for tx, ty in tower_positions:
                if tx < 60 and ty < 56:
                    for x in range(tx - 4, min(tx + 4, 64)):
                        for y in range(ty - 4, min(ty + 12, 64)):
                            self.draw_pixel(draw, x, y, stone_color, scale)
                    
                    # Crenellations
                    for x in range(tx - 4, min(tx + 4, 64), 2):
                        for y in range(ty - 6, ty - 4):
                            if y >= 0:
                                self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Gate
            for x in range(28, 36):
                for y in range(44, 52):
                    if x == 28 or x == 35 or y == 44:
                        self.draw_pixel(draw, x, y, (80, 80, 80), scale)
                    else:
                        self.draw_pixel(draw, x, y, (101, 67, 33), scale)
            
            # Banner
            banner_color = palette["buildings"][3]
            for x in range(30, 34):
                for y in range(8, 16):
                    self.draw_pixel(draw, x, y, banner_color, scale)
                    
        elif building_type == "cathedral":
            # Gothic cathedral
            stone_color = palette["buildings"][0]
            window_color = (100, 50, 200)  # Stained glass
            
            # Main structure
            for x in range(12, 52):
                for y in range(16, 56):
                    self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Twin spires
            for spire_x in [20, 44]:
                for y in range(4, 20):
                    width = max(1, 4 - (20 - y) // 3)
                    for x in range(spire_x - width, spire_x + width + 1):
                        self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Rose window
            for x in range(28, 37):
                for y in range(24, 33):
                    if ((x - 32) ** 2 + (y - 28) ** 2) ** 0.5 <= 4:
                        self.draw_pixel(draw, x, y, window_color, scale)
            
            # Gothic arched entrance
            for x in range(28, 37):
                for y in range(44, 56):
                    if x == 28 or x == 36 or y == 44:
                        self.draw_pixel(draw, x, y, stone_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, (40, 40, 40), scale)
                        
        elif building_type == "blacksmith":
            # Medieval blacksmith shop
            wood_color = palette["buildings"][1]
            stone_color = palette["buildings"][2]
            
            # Workshop building
            for x in range(12, 52):
                for y in range(24, 56):
                    # Wooden walls
                    if y % 4 == 0:
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in wood_color), scale)
                    else:
                        self.draw_pixel(draw, x, y, wood_color, scale)
            
            # Stone chimney
            for x in range(44, 52):
                for y in range(8, 28):
                    self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Smoke
            for i in range(5):
                self.draw_pixel(draw, 48 + i % 3 - 1, 7 - i, (64, 64, 64), scale)
            
            # Anvil outside
            anvil_color = (64, 64, 64)
            for x in range(18, 24):
                for y in range(48, 52):
                    self.draw_pixel(draw, x, y, anvil_color, scale)
            
            # Glowing forge visible through door
            for x in range(28, 36):
                for y in range(44, 56):
                    if x >= 30 and x <= 33 and y >= 46 and y <= 50:
                        self.draw_pixel(draw, x, y, (255, 100, 0), scale)  # Fire glow
                    else:
                        self.draw_pixel(draw, x, y, (40, 20, 10), scale)  # Dark interior

    def draw_renaissance_building(self, draw, building_type, palette, scale):
        """Draw renaissance era buildings with 64x64 detail"""
        if building_type == "mansion":
            # Ornate renaissance mansion
            wall_color = palette["buildings"][0]
            accent_color = palette["buildings"][1]
            
            # Main building with symmetry
            for x in range(8, 56):
                for y in range(20, 56):
                    self.draw_pixel(draw, x, y, wall_color, scale)
            
            # Decorative cornices
            for x in range(8, 56):
                for y in [20, 32, 44]:
                    for dy in range(2):
                        self.draw_pixel(draw, x, y + dy, accent_color, scale)
            
            # Multiple arched windows
            window_rows = [(16, 24), (16, 36), (40, 24), (40, 36)]
            for wx, wy in window_rows:
                for x in range(wx - 4, wx + 5):
                    for y in range(wy - 4, wy + 5):
                        if ((x - wx) ** 2 + (y - wy + 2) ** 2) ** 0.5 <= 4 and y > wy - 4:
                            self.draw_pixel(draw, x, y, (200, 200, 255), scale)
            
            # Grand entrance with columns
            for col_x in [24, 40]:
                for y in range(44, 56):
                    for x in range(col_x - 1, col_x + 2):
                        self.draw_pixel(draw, x, y, (245, 245, 220), scale)
            
            # Ornate roof with dome
            for x in range(24, 41):
                for y in range(8, 20):
                    if ((x - 32) ** 2 + (y - 16) ** 2) ** 0.5 <= 8:
                        self.draw_pixel(draw, x, y, accent_color, scale)
                        
        elif building_type == "university":
            # Renaissance university/academy
            stone_color = palette["buildings"][2]
            
            # Main academic building
            for x in range(8, 56):
                for y in range(16, 56):
                    self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Clock tower
            for x in range(28, 36):
                for y in range(4, 20):
                    self.draw_pixel(draw, x, y, stone_color, scale)
            
            # Clock face
            for x in range(30, 34):
                for y in range(8, 12):
                    if ((x - 32) ** 2 + (y - 10) ** 2) ** 0.5 <= 2:
                        self.draw_pixel(draw, x, y, (255, 255, 255), scale)
            self.draw_pixel(draw, 32, 10, (0, 0, 0), scale)  # Clock center
            
            # Library windows (tall and narrow)
            for window_x in range(16, 48, 8):
                for y in range(24, 48):
                    for x in range(window_x - 2, window_x + 3):
                        self.draw_pixel(draw, x, y, (180, 180, 200), scale)
                        
        elif building_type == "workshop":
            # Artist/inventor workshop
            building_color = palette["buildings"][3]
            
            # Workshop with large windows for light
            for x in range(12, 52):
                for y in range(20, 56):
                    self.draw_pixel(draw, x, y, building_color, scale)
            
            # Large workshop windows
            for x in range(16, 48):
                for y in range(24, 40):
                    if x % 8 < 6 and y % 8 < 6:
                        self.draw_pixel(draw, x, y, (220, 220, 255), scale)
            
            # Chimney for forge/kiln
            for x in range(44, 48):
                for y in range(12, 24):
                    self.draw_pixel(draw, x, y, (120, 120, 120), scale)

    def draw_modern_building(self, draw, building_type, palette, scale):
        """Draw modern era buildings with 64x64 detail"""
        if building_type == "apartment":
            # Modern apartment building
            concrete_color = palette["buildings"][0]
            glass_color = palette["buildings"][1]
            
            # Main structure
            for x in range(8, 56):
                for y in range(4, 60):
                    self.draw_pixel(draw, x, y, concrete_color, scale)
            
            # Grid of windows/balconies
            for floor in range(8, 56, 6):
                for apt in range(12, 52, 8):
                    # Window
                    for x in range(apt, apt + 6):
                        for y in range(floor, floor + 4):
                            self.draw_pixel(draw, x, y, glass_color, scale)
                    # Balcony
                    if apt < 48:
                        for x in range(apt, apt + 6):
                            self.draw_pixel(draw, x, floor + 4, (100, 100, 100), scale)
                            
        elif building_type == "mall":
            # Shopping mall
            mall_color = palette["buildings"][2]
            
            # Large rectangular structure
            for x in range(4, 60):
                for y in range(20, 56):
                    self.draw_pixel(draw, x, y, mall_color, scale)
            
            # Glass entrance
            for x in range(24, 40):
                for y in range(32, 56):
                    self.draw_pixel(draw, x, y, (150, 200, 255), scale)
            
            # Parking lot markings
            for x in range(8, 56, 8):
                for y in range(56, 60):
                    self.draw_pixel(draw, x, y, (255, 255, 255), scale)
                    
        elif building_type == "hospital":
            # Modern hospital
            hospital_color = (245, 245, 245)
            
            # Main building
            for x in range(8, 56):
                for y in range(12, 56):
                    self.draw_pixel(draw, x, y, hospital_color, scale)
            
            # Red cross
            cross_color = (255, 0, 0)
            for x in range(28, 36):
                for y in range(20, 32):
                    self.draw_pixel(draw, x, y, cross_color, scale)
            for x in range(24, 40):
                for y in range(24, 28):
                    self.draw_pixel(draw, x, y, cross_color, scale)
            
            # Emergency entrance
            for x in range(16, 24):
                for y in range(48, 56):
                    self.draw_pixel(draw, x, y, (255, 100, 100), scale)

    def draw_industrial_building(self, draw, building_type, palette, scale):
        """Draw industrial era buildings with 64x64 detail"""
        if building_type == "house":
            # Victorian-style house with detailed architecture
            brick_color = palette["buildings"][0]
            brick_dark = tuple(max(0, c - 30) for c in brick_color)
            roof_color = palette["buildings"][1]
            window_color = (255, 255, 200)
            door_color = (101, 67, 33)
            
            # Main house structure
            for x in range(8, 56):
                for y in range(24, 56):
                    # Brick pattern
                    if (x // 3 + y // 2) % 2 == 0:
                        self.draw_pixel(draw, x, y, brick_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, brick_dark, scale)
            
            # Peaked roof with shingles
            roof_peak = 12
            roof_base = 24
            for y in range(roof_peak, roof_base + 1):
                roof_width = (y - roof_peak + 1) * 3
                start_x = 32 - roof_width // 2
                for x in range(start_x, start_x + roof_width):
                    if x >= 4 and x < 60:
                        # Shingle pattern
                        if y % 3 == 0:
                            self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in roof_color), scale)
                        else:
                            self.draw_pixel(draw, x, y, roof_color, scale)
            
            # Windows with frames
            window_positions = [(16, 32), (40, 32), (16, 44), (40, 44)]
            for wx, wy in window_positions:
                # Window frame
                for x in range(wx, wx + 8):
                    for y in range(wy, wy + 8):
                        if x == wx or x == wx + 7 or y == wy or y == wy + 7:
                            self.draw_pixel(draw, x, y, (100, 100, 100), scale)
                        else:
                            self.draw_pixel(draw, x, y, window_color, scale)
            
            # Front door
            for x in range(28, 36):
                for y in range(44, 56):
                    if x == 28 or x == 35 or y == 44:
                        self.draw_pixel(draw, x, y, (80, 80, 80), scale)  # Door frame
                    else:
                        self.draw_pixel(draw, x, y, door_color, scale)
            
            # Door knob
            self.draw_pixel(draw, 34, 50, (255, 215, 0), scale)
            
            # Chimney
            for x in range(48, 52):
                for y in range(8, 20):
                    self.draw_pixel(draw, x, y, brick_color, scale)
            
            # Smoke from chimney
            smoke_positions = [(49, 7), (50, 6), (51, 5)]
            for sx, sy in smoke_positions:
                self.draw_pixel(draw, sx, sy, (128, 128, 128), scale)
            
        elif building_type == "factory":
            # Industrial factory with smokestacks
            factory_color = palette["buildings"][0]
            metal_color = (105, 105, 105)
            
            # Main factory building
            for x in range(4, 60):
                for y in range(24, 60):
                    # Industrial siding pattern
                    if y % 4 == 0:
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 20) for c in factory_color), scale)
                    else:
                        self.draw_pixel(draw, x, y, factory_color, scale)
            
            # Multiple smokestacks
            for stack_x in [16, 32, 48]:
                for x in range(stack_x - 3, stack_x + 4):
                    for y in range(4, 28):
                        self.draw_pixel(draw, x, y, metal_color, scale)
                
                # Smoke plumes
                for smoke_offset in range(-6, 7, 2):
                    smoke_x = stack_x + smoke_offset // 2
                    smoke_y = 3 - abs(smoke_offset) // 2
                    if 0 <= smoke_x < 64 and smoke_y >= 0:
                        self.draw_pixel(draw, smoke_x, smoke_y, (64, 64, 64), scale)
            
            # Factory windows (industrial style)
            for window_y in range(28, 52, 8):
                for window_x in range(8, 56, 8):
                    for x in range(window_x, window_x + 6):
                        for y in range(window_y, window_y + 6):
                            self.draw_pixel(draw, x, y, (180, 180, 180), scale)
            
            # Loading dock
            for x in range(20, 44):
                for y in range(56, 60):
                    self.draw_pixel(draw, x, y, (80, 80, 80), scale)
                
        elif building_type == "office":
            # Modern office skyscraper
            building_color = palette["buildings"][0]
            glass_color = (150, 200, 255)
            
            # Main tower
            for x in range(16, 48):
                for y in range(8, 60):
                    self.draw_pixel(draw, x, y, building_color, scale)
            
            # Glass windows in grid pattern
            for floor_y in range(12, 56, 4):
                for window_x in range(20, 44, 4):
                    for x in range(window_x, window_x + 3):
                        for y in range(floor_y, floor_y + 3):
                            self.draw_pixel(draw, x, y, glass_color, scale)
            
            # Entrance lobby
            for x in range(24, 40):
                for y in range(52, 60):
                    self.draw_pixel(draw, x, y, glass_color, scale)
            
            # Rooftop equipment
            for x in range(28, 36):
                for y in range(4, 8):
                    self.draw_pixel(draw, x, y, (120, 120, 120), scale)
    
    def draw_space_building(self, draw, building_type, palette, scale):
        """Draw space era buildings with 64x64 detail"""
        if building_type == "dome":
            # Advanced dome with multiple layers and viewports
            center_x, center_y = 32, 48
            radius = 24
            
            # Main dome structure with gradient effect
            for x in range(64):
                for y in range(64):
                    dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    if dist <= radius and y >= center_y - radius // 2:
                        # Create depth with lighter color on upper part
                        if y < center_y - 8:
                            color = tuple(min(255, c + 30) for c in palette["buildings"][0])
                        else:
                            color = palette["buildings"][0]
                        self.draw_pixel(draw, x, y, color, scale)
            
            # Viewport windows (transparent blue sections)
            viewport_color = (100, 150, 255)
            # Top viewport
            for x in range(24, 41):
                for y in range(28, 40):
                    if ((x - center_x) ** 2 + (y - 32) ** 2) ** 0.5 <= 10:
                        self.draw_pixel(draw, x, y, viewport_color, scale)
            
            # Side viewports
            for side_x in [16, 48]:
                for y in range(36, 48):
                    if abs(y - 42) <= 4:
                        self.draw_pixel(draw, side_x, y, viewport_color, scale)
            
            # Energy conduits running along the dome
            conduit_color = (0, 255, 255)
            # Vertical conduits
            for x in [20, 44]:
                for y in range(32, 52):
                    if y % 4 == 0:  # Dotted pattern
                        self.draw_pixel(draw, x, y, conduit_color, scale)
            
            # Support struts
            strut_color = (150, 150, 150)
            for strut_x in [12, 52]:
                for y in range(40, 56):
                    self.draw_pixel(draw, strut_x, y, strut_color, scale)
            
            # Advanced airlock with status lights
            airlock_color = palette["buildings"][1]
            status_light_color = (0, 255, 0)  # Green for operational
            
            for x in range(28, 37):
                for y in range(52, 64):
                    self.draw_pixel(draw, x, y, airlock_color, scale)
            
            # Status lights on airlock
            self.draw_pixel(draw, 24, 52, status_light_color, scale)
            self.draw_pixel(draw, 40, 52, status_light_color, scale)
            
            # Central antenna/communication array
            antenna_color = (200, 200, 200)
            for y in range(16, 24):
                self.draw_pixel(draw, center_x, y, antenna_color, scale)
            self.draw_pixel(draw, center_x - 4, 16, antenna_color, scale)
            self.draw_pixel(draw, center_x + 4, 16, antenna_color, scale)
                
        elif building_type == "station":
            # Modular space station with multiple sections
            station_color = palette["buildings"][0]
            panel_color = (0, 100, 200)
            docking_color = (255, 215, 0)  # Gold for docking ports
            hull_color = tuple(max(0, c - 20) for c in station_color)
            
            # Central command module (main body)
            for x in range(16, 48):
                for y in range(24, 40):
                    self.draw_pixel(draw, x, y, station_color, scale)
            
            # Upper and lower modules
            for x in range(24, 40):
                for y in range(16, 24):  # Upper module
                    self.draw_pixel(draw, x, y, hull_color, scale)
                for y in range(40, 48):  # Lower module
                    self.draw_pixel(draw, x, y, hull_color, scale)
            
            # Side docking ports with extending arms
            # Left docking port
            for x in range(8, 16):
                for y in range(28, 36):
                    self.draw_pixel(draw, x, y, docking_color, scale)
            # Right docking port  
            for x in range(48, 56):
                for y in range(28, 36):
                    self.draw_pixel(draw, x, y, docking_color, scale)
            
            # Connecting arms to docking ports
            for y in range(28, 36):
                self.draw_pixel(draw, 4, y, hull_color, scale)
                self.draw_pixel(draw, 56, y, hull_color, scale)
            
            # Extended solar panel arrays with support structures
            # Left solar array
            for x in range(0, 8):
                for y in range(20, 44):
                    if (x + y) % 2 == 0:  # Checkered pattern for cells
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, (0, 150, 255), scale)
            
            # Right solar array
            for x in range(56, 64):
                for y in range(20, 44):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, (0, 150, 255), scale)
            
            # Communication dishes/arrays
            dish_color = (180, 180, 180)
            for x in range(20, 25):
                self.draw_pixel(draw, x, 12, dish_color, scale)
            for x in range(30, 35):
                self.draw_pixel(draw, x, 8, dish_color, scale)
            for x in range(40, 45):
                self.draw_pixel(draw, x, 12, dish_color, scale)
            
            # Status lights along the hull
            light_color = (0, 255, 0)
            for x in range(16, 48, 8):
                self.draw_pixel(draw, x, 24, light_color, scale)
                self.draw_pixel(draw, x, 36, light_color, scale)
            
            # Rotating section indicators (small details)
            rotation_color = (255, 100, 100)
            self.draw_pixel(draw, 24, 32, rotation_color, scale)
            self.draw_pixel(draw, 36, 32, rotation_color, scale)
                            
        elif building_type == "lab":
            # Advanced scientific laboratory with visible equipment
            lab_color = palette["buildings"][0]
            equipment_color = (150, 150, 150)
            core_color = (0, 255, 255)
            warning_color = (255, 165, 0)
            
            # Main laboratory structure with reinforced walls
            for x in range(2, 14):
                for y in range(4, 14):
                    if x == 2 or x == 13 or y == 4 or y == 13:  # Outer walls
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 30) for c in lab_color), scale)
                    else:
                        self.draw_pixel(draw, x, y, lab_color, scale)
            
            # Central energy core with containment field
            core_center_x, core_center_y = 8, 9
            # Core itself (pulsing energy)
            for x in range(6, 11):
                for y in range(7, 11):
                    if ((x - core_center_x) ** 2 + (y - core_center_y) ** 2) ** 0.5 <= 2:
                        if (x + y) % 2 == 0:
                            self.draw_pixel(draw, x, y, core_color, scale)
                        else:
                            self.draw_pixel(draw, x, y, (0, 200, 200), scale)
            
            # Containment field generators (corners around core)
            field_color = (100, 255, 100)
            field_positions = [(5, 6), (10, 6), (5, 11), (10, 11)]
            for fx, fy in field_positions:
                self.draw_pixel(draw, fx, fy, field_color, scale)
            
            # Scientific equipment and workstations
            # Left workstation (microscopes/analyzers)
            for x in range(3, 5):
                for y in range(6, 8):
                    self.draw_pixel(draw, x, y, equipment_color, scale)
            self.draw_pixel(draw, 3, 5, (255, 255, 255), scale)  # Light/scope
            
            # Right workstation (computers/displays)
            for x in range(11, 13):
                for y in range(6, 8):
                    self.draw_pixel(draw, x, y, equipment_color, scale)
            # Computer screens
            self.draw_pixel(draw, 11, 5, (0, 255, 0), scale)  # Green display
            self.draw_pixel(draw, 12, 5, (0, 255, 0), scale)
            
            # Upper research apparatus (particle accelerator segment)
            for x in range(6, 10):
                self.draw_pixel(draw, x, 5, equipment_color, scale)
            # Particle beam
            self.draw_pixel(draw, 7, 4, (255, 255, 0), scale)
            self.draw_pixel(draw, 8, 4, (255, 255, 0), scale)
            
            # Lower equipment (sample storage/analysis)
            for x in range(5, 11):
                self.draw_pixel(draw, x, 12, equipment_color, scale)
            # Sample containers
            for sample_x in [5, 7, 9, 10]:
                self.draw_pixel(draw, sample_x, 11, (0, 255, 255), scale)
            
            # Warning lights and safety indicators
            self.draw_pixel(draw, 2, 5, warning_color, scale)
            self.draw_pixel(draw, 13, 5, warning_color, scale)
            self.draw_pixel(draw, 2, 12, warning_color, scale)
            self.draw_pixel(draw, 13, 12, warning_color, scale)
            
            # Energy conduits connecting equipment to core
            conduit_color = (0, 150, 255)
            # From core to equipment
            self.draw_pixel(draw, 5, 8, conduit_color, scale)
            self.draw_pixel(draw, 4, 7, conduit_color, scale)
            self.draw_pixel(draw, 11, 8, conduit_color, scale)
            self.draw_pixel(draw, 12, 7, conduit_color, scale)
            
            # Atmospheric processors (top corners)
            processor_color = (200, 200, 200)
            self.draw_pixel(draw, 3, 4, processor_color, scale)
            self.draw_pixel(draw, 12, 4, processor_color, scale)
            
        elif building_type == "factory":
            # Space manufacturing facility
            factory_color = palette["buildings"][0]
            machinery_color = (120, 120, 120)
            production_color = (255, 165, 0)
            
            # Main factory structure
            for x in range(1, 15):
                for y in range(5, 14):
                    self.draw_pixel(draw, x, y, factory_color, scale)
            
            # Production bays (left and right)
            for bay_x in [3, 12]:
                for y in range(7, 12):
                    self.draw_pixel(draw, bay_x, y, machinery_color, scale)
            
            # Central conveyor system
            conveyor_color = (100, 100, 100)
            for x in range(5, 11):
                self.draw_pixel(draw, x, 9, conveyor_color, scale)
                if x % 2 == 0:  # Moving parts indicator
                    self.draw_pixel(draw, x, 8, production_color, scale)
            
            # Robotic arms
            arm_color = (150, 150, 150)
            self.draw_pixel(draw, 4, 7, arm_color, scale)
            self.draw_pixel(draw, 5, 6, arm_color, scale)
            self.draw_pixel(draw, 11, 7, arm_color, scale)
            self.draw_pixel(draw, 10, 6, arm_color, scale)
            
            # Energy distributors
            energy_color = (0, 255, 255)
            for x in range(6, 10):
                self.draw_pixel(draw, x, 5, energy_color, scale)
            
            # Exhaust vents (top)
            vent_color = (80, 80, 80)
            for vent_x in [4, 8, 12]:
                for y in range(2, 5):
                    self.draw_pixel(draw, vent_x, y, vent_color, scale)
                # Heat emission
                self.draw_pixel(draw, vent_x, 1, (255, 100, 100), scale)
            
            # Status indicators
            for x in range(2, 14, 3):
                self.draw_pixel(draw, x, 6, (0, 255, 0), scale)  # Green = operational
                
        elif building_type == "habitat":
            # Living quarters for space colonists
            habitat_color = palette["buildings"][0]
            living_color = (200, 200, 255)  # Soft blue for living areas
            garden_color = (0, 255, 100)
            
            # Outer shell with radiation shielding
            for x in range(2, 14):
                for y in range(3, 15):
                    if x == 2 or x == 13 or y == 3 or y == 14:
                        # Thick outer walls
                        self.draw_pixel(draw, x, y, tuple(max(0, c - 40) for c in habitat_color), scale)
                    else:
                        self.draw_pixel(draw, x, y, habitat_color, scale)
            
            # Living compartments (residential pods)
            # Upper residential level
            for x in range(4, 7):
                for y in range(5, 8):
                    self.draw_pixel(draw, x, y, living_color, scale)
            for x in range(9, 12):
                for y in range(5, 8):
                    self.draw_pixel(draw, x, y, living_color, scale)
            
            # Lower residential level  
            for x in range(4, 7):
                for y in range(10, 13):
                    self.draw_pixel(draw, x, y, living_color, scale)
            for x in range(9, 12):
                for y in range(10, 13):
                    self.draw_pixel(draw, x, y, living_color, scale)
            
            # Central common area with hydroponics garden
            for x in range(6, 10):
                for y in range(8, 10):
                    self.draw_pixel(draw, x, y, garden_color, scale)
            
            # Life support systems
            life_support_color = (100, 255, 255)
            self.draw_pixel(draw, 3, 8, life_support_color, scale)
            self.draw_pixel(draw, 12, 8, life_support_color, scale)
            
            # Observation windows
            window_color = (150, 200, 255)
            self.draw_pixel(draw, 5, 4, window_color, scale)
            self.draw_pixel(draw, 10, 4, window_color, scale)
            self.draw_pixel(draw, 5, 13, window_color, scale)
            self.draw_pixel(draw, 10, 13, window_color, scale)
            
            # Recreation deck (top center)
            for x in range(7, 9):
                for y in range(4, 6):
                    self.draw_pixel(draw, x, y, (255, 255, 200), scale)  # Warm lighting
            
            # Atmospheric recyclers (corners)
            recycler_color = (180, 180, 180)
            self.draw_pixel(draw, 3, 4, recycler_color, scale)
            self.draw_pixel(draw, 12, 4, recycler_color, scale)
            self.draw_pixel(draw, 3, 13, recycler_color, scale)
            self.draw_pixel(draw, 12, 13, recycler_color, scale)
            
        elif building_type == "solar_array":
            # Massive solar collection facility
            panel_color = (0, 100, 200)
            panel_highlight = (0, 150, 255)
            support_color = (150, 150, 150)
            control_color = (255, 215, 0)
            
            # Central control tower
            for x in range(7, 9):
                for y in range(6, 12):
                    self.draw_pixel(draw, x, y, control_color, scale)
            
            # Main solar panel arrays (4 quadrants)
            # Top-left array
            for x in range(1, 6):
                for y in range(1, 6):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, panel_highlight, scale)
            
            # Top-right array
            for x in range(10, 15):
                for y in range(1, 6):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, panel_highlight, scale)
            
            # Bottom-left array
            for x in range(1, 6):
                for y in range(10, 15):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, panel_highlight, scale)
            
            # Bottom-right array
            for x in range(10, 15):
                for y in range(10, 15):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, panel_color, scale)
                    else:
                        self.draw_pixel(draw, x, y, panel_highlight, scale)
            
            # Support struts connecting arrays to control center
            for x in range(6, 8):  # Horizontal struts
                self.draw_pixel(draw, x, 3, support_color, scale)
                self.draw_pixel(draw, x, 12, support_color, scale)
            for x in range(9, 11):
                self.draw_pixel(draw, x, 3, support_color, scale)
                self.draw_pixel(draw, x, 12, support_color, scale)
            
            for y in range(6, 8):  # Vertical struts
                self.draw_pixel(draw, 3, y, support_color, scale)
                self.draw_pixel(draw, 12, y, support_color, scale)
            for y in range(9, 11):
                self.draw_pixel(draw, 3, y, support_color, scale)
                self.draw_pixel(draw, 12, y, support_color, scale)
            
            # Power routing indicators
            power_color = (255, 255, 0)
            # From arrays to center
            self.draw_pixel(draw, 5, 5, power_color, scale)
            self.draw_pixel(draw, 10, 5, power_color, scale)
            self.draw_pixel(draw, 5, 10, power_color, scale)
            self.draw_pixel(draw, 10, 10, power_color, scale)
            
            # Energy output indicator (center)
            self.draw_pixel(draw, 7, 8, (255, 255, 255), scale)  # High energy output
            self.draw_pixel(draw, 8, 8, (255, 255, 255), scale)
    
    def generate_vegetation_sprite(self, vegetation_type, stage, scale=1):
        """Generate vegetation sprites with growth stages and states"""
        img = self.create_image(32, 32, scale)
        draw = ImageDraw.Draw(img)
        
        if vegetation_type == "tree":
            self.draw_tree(draw, stage, scale)
        elif vegetation_type in ["wheat", "corn", "vegetables"]:
            self.draw_crop(draw, vegetation_type, stage, scale)
        elif vegetation_type == "grass_patch":
            self.draw_grass_patch(draw, stage, scale)
        elif vegetation_type == "flowers":
            self.draw_flowers(draw, stage, scale)
        elif vegetation_type == "bush":
            self.draw_bush(draw, stage, scale)
            
        return img
    
    def draw_tree(self, draw, stage, scale):
        """Draw tree in various growth stages and states"""
        if stage == "seedling":
            # Small sprout
            colors = VEGETATION_COLORS["tree"]["healthy"]
            # Tiny stem
            for y in range(26, 30):
                self.draw_pixel(draw, 16, y, colors["trunk"][0], scale)
            # Small leaves
            for x in range(15, 18):
                for y in range(24, 27):
                    if ((x - 16) ** 2 + (y - 25) ** 2) ** 0.5 <= 1.5:
                        self.draw_pixel(draw, x, y, colors["foliage"][0], scale)
                        
        elif stage == "sapling":
            # Young tree
            colors = VEGETATION_COLORS["tree"]["healthy"]
            # Trunk
            for x in range(15, 18):
                for y in range(20, 30):
                    self.draw_pixel(draw, x, y, colors["trunk"][0], scale)
            # Canopy
            for x in range(12, 21):
                for y in range(12, 22):
                    if ((x - 16) ** 2 + (y - 17) ** 2) ** 0.5 <= 5:
                        foliage_color = colors["foliage"][(x + y) % len(colors["foliage"])]
                        self.draw_pixel(draw, x, y, foliage_color, scale)
                        
        elif stage == "mature":
            # Full grown tree
            colors = VEGETATION_COLORS["tree"]["healthy"]
            # Thick trunk
            for x in range(14, 19):
                for y in range(16, 30):
                    trunk_color = colors["trunk"][(x + y) % len(colors["trunk"])]
                    self.draw_pixel(draw, x, y, trunk_color, scale)
            # Large canopy
            for x in range(8, 25):
                for y in range(4, 20):
                    if ((x - 16) ** 2 + (y - 12) ** 2) ** 0.5 <= 8:
                        foliage_color = colors["foliage"][(x + y) % len(colors["foliage"])]
                        self.draw_pixel(draw, x, y, foliage_color, scale)
                        
        elif stage == "old":
            # Old tree with sparse foliage
            colors = VEGETATION_COLORS["tree"]["healthy"]
            # Thick gnarled trunk
            for x in range(14, 19):
                for y in range(16, 30):
                    if x == 14 or x == 18 or y % 3 == 0:  # Gnarled texture
                        trunk_color = colors["trunk"][2]
                    else:
                        trunk_color = colors["trunk"][0]
                    self.draw_pixel(draw, x, y, trunk_color, scale)
            # Sparse canopy
            for x in range(8, 25):
                for y in range(4, 20):
                    if ((x - 16) ** 2 + (y - 12) ** 2) ** 0.5 <= 8 and (x + y) % 3 != 0:
                        foliage_color = colors["foliage"][(x + y) % len(colors["foliage"])]
                        self.draw_pixel(draw, x, y, foliage_color, scale)
                        
        elif stage == "dead":
            # Dead tree
            colors = VEGETATION_COLORS["tree"]["dead"]
            # Dead trunk
            for x in range(14, 19):
                for y in range(16, 30):
                    trunk_color = colors["trunk"][(x + y) % len(colors["trunk"])]
                    self.draw_pixel(draw, x, y, trunk_color, scale)
            # Dead branches with minimal foliage
            branch_positions = [(10, 10), (22, 12), (12, 14), (20, 16)]
            for bx, by in branch_positions:
                for i in range(3):
                    if 0 <= bx + i < 32 and 0 <= by < 32:
                        self.draw_pixel(draw, bx + i, by, colors["trunk"][1], scale)
                        if i == 2:  # Dead leaves at branch tips
                            self.draw_pixel(draw, bx + i, by - 1, colors["foliage"][0], scale)
                            
        elif stage == "burnt":
            # Burnt tree
            colors = VEGETATION_COLORS["tree"]["burnt"]
            # Charred trunk
            for x in range(14, 19):
                for y in range(16, 30):
                    trunk_color = colors["trunk"][(x + y) % len(colors["trunk"])]
                    self.draw_pixel(draw, x, y, trunk_color, scale)
            # Minimal burnt branches
            for x in range(12, 21):
                for y in range(8, 16):
                    if ((x - 16) ** 2 + (y - 12) ** 2) ** 0.5 <= 4 and (x + y) % 4 == 0:
                        self.draw_pixel(draw, x, y, colors["foliage"][1], scale)
    
    def draw_crop(self, draw, crop_type, stage, scale):
        """Draw crops in various growth stages"""
        colors = VEGETATION_COLORS["crops"][crop_type]
        
        if stage == "seed":
            # Seeds in soil
            for x in range(14, 19):
                for y in range(28, 30):
                    if (x + y) % 2 == 0:
                        self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        
        elif stage == "sprout":
            # Small green shoots
            for x in range(12, 21):
                for y in range(22, 30):
                    if x % 2 == 0 and y > 26:  # Soil
                        self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                    elif y < 28 and (x - 16) % 3 == 0:  # Shoots
                        self.draw_pixel(draw, x, y, colors["sprout"][0], scale)
                        
        elif stage == "growing":
            # Medium height plants
            if crop_type == "wheat":
                # Wheat stalks
                for x in range(10, 23, 2):
                    for y in range(16, 30):
                        if y > 24:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        else:  # Stalks
                            self.draw_pixel(draw, x, y, colors["growing"][0], scale)
            elif crop_type == "corn":
                # Corn stalks (taller)
                for x in range(12, 21, 3):
                    for y in range(10, 30):
                        if y > 26:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        else:  # Stalks
                            self.draw_pixel(draw, x, y, colors["growing"][0], scale)
                        # Leaves
                        if y < 20 and y % 3 == 0:
                            self.draw_pixel(draw, x - 1, y, colors["growing"][1], scale)
                            self.draw_pixel(draw, x + 1, y, colors["growing"][1], scale)
            else:  # vegetables
                # Leafy vegetables
                for x in range(8, 25):
                    for y in range(18, 30):
                        if y > 26:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        elif ((x - 16) ** 2 + (y - 22) ** 2) ** 0.5 <= 6:
                            self.draw_pixel(draw, x, y, colors["growing"][0], scale)
                            
        elif stage == "mature":
            # Ready for harvest
            if crop_type == "wheat":
                # Golden wheat ready for harvest
                for x in range(8, 25, 2):
                    for y in range(12, 30):
                        if y > 26:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        elif y < 16:  # Wheat heads
                            self.draw_pixel(draw, x, y, colors["mature"][0], scale)
                        else:  # Stalks
                            self.draw_pixel(draw, x, y, colors["mature"][1], scale)
            elif crop_type == "corn":
                # Corn with ears
                for x in range(12, 21, 3):
                    for y in range(8, 30):
                        if y > 26:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        elif y > 20:  # Lower stalk
                            self.draw_pixel(draw, x, y, colors["growing"][0], scale)
                        else:  # Upper stalk with ears
                            self.draw_pixel(draw, x, y, colors["growing"][0], scale)
                            if y == 14 or y == 18:  # Corn ears
                                for dx in range(-1, 2):
                                    self.draw_pixel(draw, x + dx, y, colors["mature"][0], scale)
            else:  # vegetables
                # Ripe vegetables
                for x in range(8, 25):
                    for y in range(16, 30):
                        if y > 26:  # Soil
                            self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                        elif ((x - 16) ** 2 + (y - 22) ** 2) ** 0.5 <= 7:
                            if (x + y) % 3 == 0:  # Vegetables/fruits
                                self.draw_pixel(draw, x, y, colors["mature"][1], scale)
                            else:  # Leaves
                                self.draw_pixel(draw, x, y, colors["mature"][0], scale)
                                
        elif stage == "dead":
            # Withered crops
            for x in range(10, 23):
                for y in range(20, 30):
                    if y > 26:  # Soil
                        self.draw_pixel(draw, x, y, colors["seed"][0], scale)
                    elif (x + y) % 3 == 0:  # Sparse dead vegetation
                        self.draw_pixel(draw, x, y, colors["dead"][0], scale)
    
    def draw_grass_patch(self, draw, stage, scale):
        """Draw grass patches in various states"""
        colors = VEGETATION_COLORS["grass"]
        
        if stage == "healthy":
            # Lush green grass
            for x in range(32):
                for y in range(24, 32):
                    if (x * 3 + y) % 4 != 0:  # Grass density
                        grass_color = colors["healthy"][(x + y) % len(colors["healthy"])]
                        self.draw_pixel(draw, x, y, grass_color, scale)
            # Individual grass blades
            for i in range(20):
                gx = (i * 7) % 32
                gy = 20 + (i * 3) % 8
                for j in range(3):
                    if gy + j < 32:
                        self.draw_pixel(draw, gx, gy + j, colors["healthy"][0], scale)
                        
        elif stage == "dry":
            # Dry/yellow grass
            for x in range(32):
                for y in range(26, 32):
                    if (x * 2 + y) % 3 != 0:  # Sparser
                        grass_color = colors["dry"][(x + y) % len(colors["dry"])]
                        self.draw_pixel(draw, x, y, grass_color, scale)
                        
        elif stage == "dead":
            # Brown dead grass
            for x in range(32):
                for y in range(28, 32):
                    if (x + y) % 2 == 0:  # Very sparse
                        grass_color = colors["dead"][(x + y) % len(colors["dead"])]
                        self.draw_pixel(draw, x, y, grass_color, scale)
                        
        elif stage == "burnt":
            # Charred grass patches
            for x in range(32):
                for y in range(30, 32):
                    if (x * 5 + y) % 7 == 0:  # Very sparse burnt patches
                        grass_color = colors["burnt"][(x + y) % len(colors["burnt"])]
                        self.draw_pixel(draw, x, y, grass_color, scale)
    
    def draw_flowers(self, draw, stage, scale):
        """Draw flowers in various states"""
        colors = VEGETATION_COLORS["flowers"]
        
        if stage == "healthy":
            # Colorful flowers
            flower_positions = [(8, 20), (16, 18), (24, 22), (12, 26), (20, 24)]
            for i, (fx, fy) in enumerate(flower_positions):
                # Stem
                for y in range(fy, min(fy + 8, 32)):
                    self.draw_pixel(draw, fx, y, colors["healthy"][3], scale)  # Green stem
                # Flower petals
                petal_color = colors["healthy"][i % 3]  # Different colored flowers
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if abs(dx) + abs(dy) <= 2:
                            px, py = fx + dx, fy + dy
                            if 0 <= px < 32 and 0 <= py < 32:
                                self.draw_pixel(draw, px, py, petal_color, scale)
                # Flower center
                self.draw_pixel(draw, fx, fy, (255, 255, 0), scale)
                
        elif stage == "wilted":
            # Drooping flowers
            flower_positions = [(10, 24), (18, 26), (14, 28)]
            for fx, fy in flower_positions:
                # Drooping stem
                for y in range(fy, min(fy + 6, 32)):
                    self.draw_pixel(draw, fx + (y - fy), y, colors["wilted"][0], scale)
                # Wilted petals
                self.draw_pixel(draw, fx, fy, colors["wilted"][1], scale)
                self.draw_pixel(draw, fx - 1, fy + 1, colors["wilted"][1], scale)
                
        elif stage == "dead":
            # Dead flower remnants
            for x in range(8, 25, 4):
                for y in range(26, 30):
                    if (x + y) % 3 == 0:
                        self.draw_pixel(draw, x, y, colors["dead"][0], scale)
    
    def draw_bush(self, draw, stage, scale):
        """Draw bushes in various states"""
        if stage == "healthy":
            # Green bush
            bush_color = VEGETATION_COLORS["tree"]["healthy"]["foliage"]
            for x in range(8, 24):
                for y in range(16, 28):
                    if ((x - 16) ** 2 + (y - 22) ** 2) ** 0.5 <= 8:
                        color = bush_color[(x + y) % len(bush_color)]
                        self.draw_pixel(draw, x, y, color, scale)
        elif stage == "autumn":
            # Autumn colors
            bush_color = VEGETATION_COLORS["tree"]["autumn"]["foliage"]
            for x in range(8, 24):
                for y in range(16, 28):
                    if ((x - 16) ** 2 + (y - 22) ** 2) ** 0.5 <= 8:
                        color = bush_color[(x + y) % len(bush_color)]
                        self.draw_pixel(draw, x, y, color, scale)
        elif stage == "dead":
            # Dead bush
            bush_color = VEGETATION_COLORS["tree"]["dead"]["foliage"]
            for x in range(10, 22):
                for y in range(18, 26):
                    if ((x - 16) ** 2 + (y - 22) ** 2) ** 0.5 <= 6 and (x + y) % 2 == 0:
                        color = bush_color[(x + y) % len(bush_color)]
                        self.draw_pixel(draw, x, y, color, scale)

    def generate_terrain_tile(self, terrain_type, scale=1):
        """Generate a 32x32 terrain tile"""
        img = self.create_image(32, 32, scale)
        draw = ImageDraw.Draw(img)
        base_color = TERRAIN_COLORS[terrain_type]
        
        if terrain_type == "grass":
            # Fill with grass color with detailed texture
            for x in range(32):
                for y in range(32):
                    # Add variation and texture
                    variation = (x * 3 + y * 2) % 5 - 2
                    color = (
                        max(0, min(255, base_color[0] + variation * 8)),
                        max(0, min(255, base_color[1] + variation * 8)),
                        max(0, min(255, base_color[2] + variation * 8))
                    )
                    self.draw_pixel(draw, x, y, color, scale)
            
            # Add grass blade details
            blade_color = (0, 120, 0)
            for i in range(15):
                bx = (i * 7) % 32
                by = (i * 11) % 32
                for j in range(3):
                    if by + j < 32:
                        self.draw_pixel(draw, bx, by + j, blade_color, scale)
        
        elif terrain_type == "water":
            # Water with detailed wave pattern
            for x in range(32):
                for y in range(32):
                    # Wave effect
                    wave = int(math.sin(x * 0.3 + y * 0.1) * 15)
                    color = (
                        max(0, min(255, base_color[0] + wave)),
                        max(0, min(255, base_color[1] + wave + 10)),
                        max(0, min(255, base_color[2] + wave + 20))
                    )
                    self.draw_pixel(draw, x, y, color, scale)
            
            # Add foam/whitecaps
            foam_color = (200, 220, 255)
            for i in range(8):
                fx = (i * 13) % 32
                fy = (i * 7) % 32
                self.draw_pixel(draw, fx, fy, foam_color, scale)
                if fx + 1 < 32:
                    self.draw_pixel(draw, fx + 1, fy, foam_color, scale)
        
        elif terrain_type == "forest":
            # Dense forest floor
            for x in range(32):
                for y in range(32):
                    # Forest floor variation
                    variation = (x + y * 2) % 4 - 2
                    color = (
                        max(0, min(255, base_color[0] + variation * 10)),
                        max(0, min(255, base_color[1] + variation * 10)),
                        max(0, min(255, base_color[2] + variation * 10))
                    )
                    self.draw_pixel(draw, x, y, color, scale)
            
            # Multiple detailed trees
            tree_positions = [(8, 8), (20, 12), (5, 20), (25, 6), (15, 24), (28, 18)]
            for tx, ty in tree_positions:
                # Tree trunk
                trunk_color = (101, 67, 33)
                for x in range(tx - 1, tx + 2):
                    for y in range(ty, min(ty + 6, 32)):
                        if x >= 0 and x < 32:
                            self.draw_pixel(draw, x, y, trunk_color, scale)
                
                # Tree canopy
                canopy_color = (0, 80, 0)
                for x in range(tx - 3, tx + 4):
                    for y in range(ty - 4, ty + 1):
                        if x >= 0 and x < 32 and y >= 0 and y < 32:
                            if ((x - tx) ** 2 + (y - ty + 2) ** 2) ** 0.5 <= 3.5:
                                self.draw_pixel(draw, x, y, canopy_color, scale)
        
        else:
            # Default: fill with base color and add texture
            for x in range(32):
                for y in range(32):
                    # Generic texture pattern
                    texture = ((x // 4) + (y // 4)) % 2
                    color_mod = -10 if texture else 0
                    color = (
                        max(0, min(255, base_color[0] + color_mod)),
                        max(0, min(255, base_color[1] + color_mod)),
                        max(0, min(255, base_color[2] + color_mod))
                    )
                    self.draw_pixel(draw, x, y, color, scale)
        
        return img
    
    def generate_effect_sprite(self, effect_type, frame=0, scale=1):
        """Generate effect sprites (explosions, smoke, etc.)"""
        img = self.create_image(48, 48, scale)
        draw = ImageDraw.Draw(img)
        
        if effect_type == "explosion":
            # Detailed explosion animation
            colors = [(255, 255, 255), (255, 255, 0), (255, 165, 0), (255, 69, 0), (128, 128, 128)]
            
            center_x, center_y = 24, 24
            radius = min(frame * 4 + 8, 20)
            
            for x in range(48):
                for y in range(48):
                    dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    if dist <= radius:
                        # More complex explosion pattern
                        color_idx = min(int(dist / 4), len(colors) - 1)
                        # Add some randomness to the explosion
                        if frame > 1 and (x + y) % 3 == 0:
                            color_idx = min(color_idx + 1, len(colors) - 1)
                        self.draw_pixel(draw, x, y, colors[color_idx], scale)
                    
                    # Explosion debris/sparks
                    if frame > 0 and dist > radius - 4 and dist < radius + 2:
                        if (x * y + frame) % 5 == 0:
                            self.draw_pixel(draw, x, y, (255, 200, 0), scale)
        
        elif effect_type == "smoke":
            # Rising smoke particles with volume
            smoke_base_color = (128, 128, 128)
            
            # Multiple smoke clouds
            for cloud in range(3):
                cloud_x = 24 + (cloud - 1) * 8
                cloud_y = 40 - frame * 6 - cloud * 4
                
                # Draw volumetric smoke cloud
                for x in range(max(0, cloud_x - 8), min(48, cloud_x + 8)):
                    for y in range(max(0, cloud_y - 8), min(48, cloud_y + 8)):
                        dist = ((x - cloud_x) ** 2 + (y - cloud_y) ** 2) ** 0.5
                        if dist <= 8:
                            # Fade based on distance and frame
                            opacity = int(255 * (1 - dist / 8) * (1 - frame / 4))
                            if opacity > 0:
                                gray_value = 128 + int((dist / 8) * 40)
                                color = (gray_value, gray_value, gray_value)
                                self.draw_pixel(draw, x, y, color, scale)
        
        elif effect_type == "sparkle":
            # Large magical sparkle effect
            sparkle_color = (255, 255, 255)
            star_color = (255, 255, 200)
            center_x, center_y = 24, 24
            
            # Different sparkle patterns per frame
            if frame == 0:
                # Small center spark
                for x in range(center_x - 2, center_x + 3):
                    for y in range(center_y - 2, center_y + 3):
                        self.draw_pixel(draw, x, y, sparkle_color, scale)
            elif frame == 1:
                # Medium star pattern
                # Center
                for x in range(center_x - 3, center_x + 4):
                    for y in range(center_y - 3, center_y + 4):
                        self.draw_pixel(draw, x, y, sparkle_color, scale)
                # Star points
                for i in range(1, 8):
                    self.draw_pixel(draw, center_x - i, center_y, star_color, scale)
                    self.draw_pixel(draw, center_x + i, center_y, star_color, scale)
                    self.draw_pixel(draw, center_x, center_y - i, star_color, scale)
                    self.draw_pixel(draw, center_x, center_y + i, star_color, scale)
            elif frame == 2:
                # Large star burst
                for i in range(-12, 13):
                    if abs(i) > 2:
                        self.draw_pixel(draw, center_x + i, center_y, star_color, scale)
                        self.draw_pixel(draw, center_x, center_y + i, star_color, scale)
                    # Diagonal rays
                    if abs(i) > 4 and abs(i) < 10:
                        self.draw_pixel(draw, center_x + i, center_y + i, star_color, scale)
                        self.draw_pixel(draw, center_x + i, center_y - i, star_color, scale)
                # Bright center
                for x in range(center_x - 2, center_x + 3):
                    for y in range(center_y - 2, center_y + 3):
                        self.draw_pixel(draw, x, y, sparkle_color, scale)
            elif frame == 3:
                # Fade out with particles
                fade_positions = [
                    (center_x, center_y), (center_x - 6, center_y - 6),
                    (center_x + 6, center_y - 6), (center_x - 6, center_y + 6),
                    (center_x + 6, center_y + 6), (center_x - 10, center_y),
                    (center_x + 10, center_y), (center_x, center_y - 10),
                    (center_x, center_y + 10)
                ]
                for fx, fy in fade_positions:
                    if 0 <= fx < 48 and 0 <= fy < 48:
                        self.draw_pixel(draw, fx, fy, (255, 255, 255), scale)
        
        return img
    
    def generate_fire_sprite(self, fire_type, frame, scale=1):
        """Generate fire sprites with animation frames and spreading effects"""
        if fire_type in ["ignition", "small", "medium", "large", "dying"]:
            img = self.create_image(48, 48, scale)  # Fire sprites are 48x48
        else:
            img = self.create_image(32, 32, scale)  # Embers and smoke are 32x32
        draw = ImageDraw.Draw(img)
        
        if fire_type in ["ignition", "small", "medium", "large", "dying"]:
            self.draw_fire(draw, fire_type, frame, scale)
        elif fire_type == "ember":
            self.draw_ember(draw, frame, scale)
        elif fire_type == "smoke":
            self.draw_smoke(draw, frame, scale)
            
        return img
    
    def draw_fire(self, draw, intensity, frame, scale):
        """Draw fire with realistic flames and animation"""
        colors = FIRE_COLORS[intensity]
        center_x, center_y = 24, 36  # Bottom center of 48x48 canvas
        
        # Base fire shape varies by intensity
        if intensity == "ignition":
            height = 12 + frame * 2
            width = 8 + frame
        elif intensity == "small":
            height = 16 + frame * 3
            width = 12 + frame * 2
        elif intensity == "medium":
            height = 24 + frame * 4
            width = 18 + frame * 3
        elif intensity == "large":
            height = 32 + frame * 5
            width = 24 + frame * 4
        else:  # dying
            height = 8 + frame
            width = 6 + frame
        
        # Draw flame core (bottom to top, getting narrower)
        for y in range(center_y, max(0, center_y - height), -1):
            flame_width = int(width * (center_y - y + 1) / height)
            for x in range(center_x - flame_width // 2, center_x + flame_width // 2 + 1):
                if 0 <= x < 48 and 0 <= y < 48:
                    # Flame shape with some randomness based on position
                    distance_from_center = abs(x - center_x)
                    heat_level = (center_y - y) / height
                    
                    # Choose color based on distance from center and height
                    if distance_from_center < flame_width // 4:
                        # Core of flame - hottest
                        color = colors["core"][(x + y + frame) % len(colors["core"])]
                    elif distance_from_center < flame_width // 2:
                        # Outer flame
                        color = colors["outer"][(x + y + frame) % len(colors["outer"])]
                    else:
                        # Edge - might be empty for flame effect
                        if (x + y + frame) % 3 == 0:
                            color = colors["outer"][0]
                        else:
                            continue
                    
                    self.draw_pixel(draw, x, y, color, scale)
        
        # Add flickering sparks above flame
        spark_count = 3 + frame % 3
        for i in range(spark_count):
            spark_x = center_x + (i - spark_count // 2) * 4 + frame % 3
            spark_y = center_y - height - 5 - i * 2 - frame % 4
            if 0 <= spark_x < 48 and 0 <= spark_y < 48:
                spark_color = colors["sparks"][i % len(colors["sparks"])]
                self.draw_pixel(draw, spark_x, spark_y, spark_color, scale)
                
        # Add dancing flame tips for larger fires
        if intensity in ["medium", "large"]:
            tip_positions = [
                (center_x - 6, center_y - height + frame % 4),
                (center_x + 6, center_y - height + (frame + 1) % 4),
                (center_x, center_y - height - 2 + (frame + 2) % 3)
            ]
            for tx, ty in tip_positions:
                if 0 <= tx < 48 and 0 <= ty < 48:
                    self.draw_pixel(draw, tx, ty, colors["outer"][0], scale)
    
    def draw_ember(self, draw, frame, scale):
        """Draw glowing embers for fire spread"""
        colors = FIRE_COLORS["embers"]
        
        # Multiple small glowing particles
        ember_positions = [
            (8, 8), (24, 12), (16, 20), (28, 24), (12, 28),
            (20, 6), (6, 16), (26, 18), (14, 24), (22, 30)
        ]
        
        for i, (ex, ey) in enumerate(ember_positions):
            # Animate embers by changing their intensity
            intensity_cycle = (frame + i) % 6
            if intensity_cycle < 2:
                color = colors["hot"][i % len(colors["hot"])]
                size = 2
            elif intensity_cycle < 4:
                color = colors["warm"][i % len(colors["warm"])]
                size = 1
            else:
                color = colors["cool"][i % len(colors["cool"])]
                size = 1
                
            # Draw ember with slight glow
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    nx, ny = ex + dx, ey + dy
                    if 0 <= nx < 32 and 0 <= ny < 32:
                        if dx == 0 and dy == 0:
                            self.draw_pixel(draw, nx, ny, color, scale)
                        elif abs(dx) + abs(dy) == 1:
                            # Dimmer glow around ember
                            glow_color = tuple(max(0, c - 50) for c in color)
                            self.draw_pixel(draw, nx, ny, glow_color, scale)
    
    def draw_smoke(self, draw, frame, scale):
        """Draw smoke animation frames"""
        colors = FIRE_COLORS["smoke"]
        
        # Smoke starts thick at bottom and becomes wispy at top
        for y in range(32):
            smoke_density = max(0, 32 - y) / 32
            
            for x in range(32):
                # Create wavy smoke pattern
                wave_offset = int(math.sin((x + frame) * 0.3) * 3)
                drift_offset = frame % 8
                smoke_x = x + wave_offset + drift_offset
                
                if 0 <= smoke_x < 32:
                    # Determine smoke thickness based on position
                    distance_from_center = abs(x - 16)
                    
                    if smoke_density > 0.7 and distance_from_center < 8:
                        # Thick smoke
                        if (x + y + frame) % 4 == 0:
                            color = colors["thick"][(x + y) % len(colors["thick"])]
                            self.draw_pixel(draw, smoke_x, y, color, scale)
                    elif smoke_density > 0.4 and distance_from_center < 12:
                        # Light smoke
                        if (x + y + frame) % 3 == 0:
                            color = colors["light"][(x + y) % len(colors["light"])]
                            self.draw_pixel(draw, smoke_x, y, color, scale)
                    elif smoke_density > 0.1 and distance_from_center < 16:
                        # Wispy smoke
                        if (x + y + frame) % 5 == 0:
                            color = colors["wispy"][(x + y) % len(colors["wispy"])]
                            self.draw_pixel(draw, smoke_x, y, color, scale)
    
    def generate_all_sprites(self):
        """Generate all placeholder sprites"""
        print("Generating sprites...")
        
        # Generate units for each era
        for era in ["primitive", "ancient", "medieval", "renaissance", "industrial", "modern", "space"]:
            print(f"Generating {era} era sprites...")
            
            # Unit types
            for unit_type in ["basic", "leader", "worker", "warrior"]:
                sprite = self.generate_unit_sprite(era, unit_type)
                sprite.save(self.output_dir / era / f"unit_{unit_type}.png")
            
            # Buildings
            building_types = {
                "primitive": ["hut", "tent", "shrine"],
                "ancient": ["villa", "temple", "forum"],
                "medieval": ["castle", "cathedral", "blacksmith"],
                "renaissance": ["mansion", "university", "workshop"],
                "industrial": ["house", "factory", "office"],
                "modern": ["apartment", "mall", "hospital"],
                "space": ["dome", "station", "lab", "factory", "habitat", "solar_array"]
            }
            
            for building in building_types[era]:
                sprite = self.generate_building_sprite(era, building)
                sprite.save(self.output_dir / era / f"building_{building}.png")
        
        # Generate terrain tiles
        print("Generating terrain tiles...")
        for terrain in TERRAIN_COLORS.keys():
            sprite = self.generate_terrain_tile(terrain)
            sprite.save(self.output_dir / "terrain" / f"{terrain}.png")
        
        # Generate effect sprites
        print("Generating effect sprites...")
        for effect in ["explosion", "smoke", "sparkle"]:
            for frame in range(4):
                sprite = self.generate_effect_sprite(effect, frame)
                sprite.save(self.output_dir / "effects" / f"{effect}_frame_{frame}.png")
        
        # Generate vegetation sprites
        print("Generating vegetation sprites...")
        
        # Tree growth stages and states
        tree_stages = ["seedling", "sapling", "mature", "old", "dead", "burnt"]
        for stage in tree_stages:
            sprite = self.generate_vegetation_sprite("tree", stage)
            sprite.save(self.output_dir / "vegetation" / f"tree_{stage}.png")
        
        # Crop types and stages
        crop_types = ["wheat", "corn", "vegetables"]
        crop_stages = ["seed", "sprout", "growing", "mature", "dead"]
        for crop in crop_types:
            for stage in crop_stages:
                sprite = self.generate_vegetation_sprite(crop, stage)
                sprite.save(self.output_dir / "vegetation" / f"{crop}_{stage}.png")
        
        # Grass patch states
        grass_stages = ["healthy", "dry", "dead", "burnt"]
        for stage in grass_stages:
            sprite = self.generate_vegetation_sprite("grass_patch", stage)
            sprite.save(self.output_dir / "vegetation" / f"grass_{stage}.png")
        
        # Flower states
        flower_stages = ["healthy", "wilted", "dead"]
        for stage in flower_stages:
            sprite = self.generate_vegetation_sprite("flowers", stage)
            sprite.save(self.output_dir / "vegetation" / f"flowers_{stage}.png")
        
        # Bush states
        bush_stages = ["healthy", "autumn", "dead"]
        for stage in bush_stages:
            sprite = self.generate_vegetation_sprite("bush", stage)
            sprite.save(self.output_dir / "vegetation" / f"bush_{stage}.png")
        
        # Generate fire sprites
        print("Generating fire sprites...")
        
        # Fire intensity levels with animation frames (4 frames each)
        fire_intensities = ["ignition", "small", "medium", "large", "dying"]
        for intensity in fire_intensities:
            for frame in range(4):
                sprite = self.generate_fire_sprite(intensity, frame)
                sprite.save(self.output_dir / "fire" / f"fire_{intensity}_frame_{frame}.png")
        
        # Ember animation frames (6 frames for spreading effect)
        for frame in range(6):
            sprite = self.generate_fire_sprite("ember", frame)
            sprite.save(self.output_dir / "fire" / f"ember_frame_{frame}.png")
        
        # Smoke animation frames (8 frames for drifting effect)
        for frame in range(8):
            sprite = self.generate_fire_sprite("smoke", frame)
            sprite.save(self.output_dir / "fire" / f"smoke_frame_{frame}.png")
        
        print(f"All sprites generated in {self.output_dir}")
    
    def generate_sprite_atlas_info(self):
        """Generate atlas information for Godot"""
        atlas_info = {
            "units": {},
            "buildings": {},
            "terrain": {},
            "effects": {},
            "vegetation": {},
            "fire": {}
        }
        
        # Scan generated sprites and create atlas info
        for era in ["primitive", "ancient", "medieval", "renaissance", "industrial", "modern", "space"]:
            atlas_info["units"][era] = []
            atlas_info["buildings"][era] = []
            
            era_path = self.output_dir / era
            if era_path.exists():
                for sprite_file in era_path.glob("*.png"):
                    sprite_type = sprite_file.stem.split("_")[0]
                    sprite_name = sprite_file.stem.split("_", 1)[1]
                    
                    sprite_info = {
                        "name": sprite_name,
                        "file": str(sprite_file.relative_to(self.output_dir)),
                        "size": [64, 64] if sprite_type == "unit" else [64, 64]  # Updated sizes
                    }
                    
                    atlas_info[sprite_type + "s"][era].append(sprite_info)
        
        # Terrain atlas info
        terrain_path = self.output_dir / "terrain"
        atlas_info["terrain"] = []
        if terrain_path.exists():
            for sprite_file in terrain_path.glob("*.png"):
                atlas_info["terrain"].append({
                    "name": sprite_file.stem,
                    "file": str(sprite_file.relative_to(self.output_dir)),
                    "size": [32, 32]
                })
        
        # Effects atlas info
        effects_path = self.output_dir / "effects"
        atlas_info["effects"] = []
        if effects_path.exists():
            for sprite_file in effects_path.glob("*.png"):
                atlas_info["effects"].append({
                    "name": sprite_file.stem,
                    "file": str(sprite_file.relative_to(self.output_dir)),
                    "size": [48, 48]
                })
        
        # Vegetation atlas info
        vegetation_path = self.output_dir / "vegetation"
        atlas_info["vegetation"] = []
        if vegetation_path.exists():
            for sprite_file in vegetation_path.glob("*.png"):
                atlas_info["vegetation"].append({
                    "name": sprite_file.stem,
                    "file": str(sprite_file.relative_to(self.output_dir)),
                    "size": [32, 32]
                })
        
        # Fire sprites
        fire_path = self.output_dir / "fire"
        atlas_info["fire"] = []
        if fire_path.exists():
            for sprite_file in fire_path.glob("*.png"):
                # Fire sprites have different sizes (fire: 48x48, ember/smoke: 32x32)
                if "fire_" in sprite_file.name:
                    size = [48, 48]
                else:
                    size = [32, 32]
                atlas_info["fire"].append({
                    "name": sprite_file.stem,
                    "file": str(sprite_file.relative_to(self.output_dir)),
                    "size": size
                })
        
        # Save atlas info
        with open(self.output_dir / "sprite_atlas.json", "w") as f:
            json.dump(atlas_info, f, indent=2)
        
        print(f"Atlas info saved to {self.output_dir / 'sprite_atlas.json'}")

def main():
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "oneiric-parallax/sprites"
    
    generator = SpriteGenerator(output_dir)
    generator.generate_all_sprites()
    generator.generate_sprite_atlas_info()
    
    print("\n✓ Sprite generation complete!")
    print(f"  Generated sprites in: {generator.output_dir}")
    print("  Ready for import into Godot!")

if __name__ == "__main__":
    main()