#!/usr/bin/env python3
"""
Sprite Test Script
Creates a visual overview of all generated sprites
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

def create_sprite_overview():
    """Create a combined image showing all sprites"""
    sprite_dir = Path("oneiric-parallax/sprites")
    
    if not sprite_dir.exists():
        print("❌ Sprites directory not found!")
        return
    
    # Create a large canvas
    overview_width = 900
    overview_height = 1000
    overview = Image.new('RGB', (overview_width, overview_height), (50, 50, 50))
    draw = ImageDraw.Draw(overview)
    
    x_pos = 10
    y_pos = 10
    
    # Add title
    draw.text((10, 10), "Cosmic Civilization Game - Sprite Overview", fill=(255, 255, 255))
    y_pos += 30
    
    # Process each era
    for era in ["primitive", "industrial", "space"]:
        era_path = sprite_dir / era
        if era_path.exists():
            # Era title
            draw.text((x_pos, y_pos), f"{era.upper()} ERA:", fill=(255, 255, 255))
            y_pos += 20
            
            era_x = x_pos + 20
            era_y = y_pos
            
            # Units
            draw.text((era_x, era_y), "Units:", fill=(200, 200, 200))
            era_y += 15
            
            sprite_x = era_x + 10
            for unit_type in ["basic", "leader", "warrior", "worker"]:
                sprite_file = era_path / f"unit_{unit_type}.png"
                if sprite_file.exists():
                    try:
                        sprite = Image.open(sprite_file)
                        overview.paste(sprite, (sprite_x, era_y), sprite)
                        draw.text((sprite_x, era_y + sprite.height + 2), unit_type[:4], fill=(150, 150, 150))
                        sprite_x += sprite.width + 40
                    except Exception as e:
                        print(f"❌ Error loading {sprite_file}: {e}")
                        
            era_y += 50
            
            # Buildings
            draw.text((era_x, era_y), "Buildings:", fill=(200, 200, 200))
            era_y += 15
            
            sprite_x = era_x + 10
            building_types = {
                "primitive": ["hut", "tent", "shrine"],
                "industrial": ["house", "factory", "office"],
                "space": ["dome", "station", "lab"]
            }
            
            for building in building_types[era]:
                sprite_file = era_path / f"building_{building}.png"
                if sprite_file.exists():
                    try:
                        sprite = Image.open(sprite_file)
                        overview.paste(sprite, (sprite_x, era_y), sprite)
                        draw.text((sprite_x, era_y + sprite.height + 2), building[:4], fill=(150, 150, 150))
                        sprite_x += sprite.width + 40
                    except Exception as e:
                        print(f"❌ Error loading {sprite_file}: {e}")
            
            y_pos += 120
    
    # Terrain section
    terrain_path = sprite_dir / "terrain"
    if terrain_path.exists():
        draw.text((x_pos, y_pos), "TERRAIN:", fill=(255, 255, 255))
        y_pos += 20
        
        sprite_x = x_pos + 20
        for terrain_file in sorted(terrain_path.glob("*.png")):
            try:
                sprite = Image.open(terrain_file)
                overview.paste(sprite, (sprite_x, y_pos), sprite)
                draw.text((sprite_x, y_pos + sprite.height + 2), terrain_file.stem[:4], fill=(150, 150, 150))
                sprite_x += sprite.width + 40
                
                if sprite_x > overview_width - 50:
                    sprite_x = x_pos + 20
                    y_pos += 50
            except Exception as e:
                print(f"❌ Error loading {terrain_file}: {e}")
        
        y_pos += 80
    
    # Vegetation section
    vegetation_path = sprite_dir / "vegetation"
    if vegetation_path.exists():
        draw.text((x_pos, y_pos), "VEGETATION:", fill=(255, 255, 255))
        y_pos += 20
        
        # Group vegetation by type
        vegetation_groups = {
            "TREES": ["tree_seedling", "tree_sapling", "tree_mature", "tree_old", "tree_dead", "tree_burnt"],
            "CROPS": ["wheat_seed", "wheat_sprout", "wheat_growing", "wheat_mature", "wheat_dead",
                     "corn_seed", "corn_sprout", "corn_growing", "corn_mature", "corn_dead",
                     "vegetables_seed", "vegetables_sprout", "vegetables_growing", "vegetables_mature", "vegetables_dead"],
            "NATURE": ["grass_healthy", "grass_dry", "grass_dead", "grass_burnt",
                      "flowers_healthy", "flowers_wilted", "flowers_dead",
                      "bush_healthy", "bush_autumn", "bush_dead"]
        }
        
        for group_name, sprite_names in vegetation_groups.items():
            draw.text((x_pos + 20, y_pos), group_name + ":", fill=(200, 200, 200))
            y_pos += 15
            
            sprite_x = x_pos + 40
            row_height = 0
            for sprite_name in sprite_names:
                sprite_file = vegetation_path / f"{sprite_name}.png"
                if sprite_file.exists():
                    try:
                        sprite = Image.open(sprite_file)
                        overview.paste(sprite, (sprite_x, y_pos), sprite)
                        # Shorter labels for vegetation
                        label = sprite_name.split('_')[1][:3]
                        draw.text((sprite_x, y_pos + sprite.height + 2), label, fill=(150, 150, 150))
                        sprite_x += sprite.width + 20
                        row_height = max(row_height, sprite.height)
                        
                        if sprite_x > overview_width - 50:
                            sprite_x = x_pos + 40
                            y_pos += row_height + 20
                            row_height = 0
                    except Exception as e:
                        print(f"❌ Error loading {sprite_file}: {e}")
            
            y_pos += row_height + 30
    
    # Fire section
    fire_path = sprite_dir / "fire"
    if fire_path.exists():
        draw.text((x_pos, y_pos), "FIRE SYSTEM:", fill=(255, 255, 255))
        y_pos += 20
        
        # Group fire sprites by type
        fire_groups = {
            "FIRE ANIMATION": ["fire_ignition_frame_0", "fire_small_frame_0", "fire_medium_frame_0", "fire_large_frame_0", "fire_dying_frame_0"],
            "EMBERS": ["ember_frame_0", "ember_frame_1", "ember_frame_2", "ember_frame_3", "ember_frame_4", "ember_frame_5"],
            "SMOKE": ["smoke_frame_0", "smoke_frame_2", "smoke_frame_4", "smoke_frame_6"]
        }
        
        for group_name, sprite_names in fire_groups.items():
            draw.text((x_pos + 20, y_pos), group_name + ":", fill=(200, 200, 200))
            y_pos += 15
            
            sprite_x = x_pos + 40
            row_height = 0
            for sprite_name in sprite_names:
                sprite_file = fire_path / f"{sprite_name}.png"
                if sprite_file.exists():
                    try:
                        sprite = Image.open(sprite_file)
                        overview.paste(sprite, (sprite_x, y_pos), sprite)
                        # Shorter labels for fire
                        if "fire_" in sprite_name:
                            label = sprite_name.split('_')[1][:3]  # ignition -> ign, small -> sma, etc
                        else:
                            label = sprite_name.split('_')[0][:3]  # ember -> emb, smoke -> smo
                        draw.text((sprite_x, y_pos + sprite.height + 2), label, fill=(150, 150, 150))
                        sprite_x += sprite.width + 20
                        row_height = max(row_height, sprite.height)
                        
                        if sprite_x > overview_width - 60:
                            sprite_x = x_pos + 40
                            y_pos += row_height + 20
                            row_height = 0
                    except Exception as e:
                        print(f"❌ Error loading {sprite_file}: {e}")
            
            y_pos += row_height + 30
    
    # Save overview
    overview.save("sprite_overview.png")
    print("✅ Sprite overview saved as 'sprite_overview.png'")
    
    # Check sprite quality
    check_sprite_quality()

def check_sprite_quality():
    """Check each sprite for common issues"""
    sprite_dir = Path("oneiric-parallax/sprites")
    issues = []
    good_sprites = 0
    
    for sprite_file in sprite_dir.rglob("*.png"):
        try:
            with Image.open(sprite_file) as img:
                # Check if image is not empty
                if img.size == (0, 0):
                    issues.append(f"❌ {sprite_file.name}: Empty image")
                    continue
                
                # Check if image has any non-transparent pixels
                if img.mode == 'RGBA':
                    # Get alpha channel
                    alpha = img.split()[-1]
                    if alpha.getextrema()[1] == 0:  # All pixels are transparent
                        issues.append(f"⚠️  {sprite_file.name}: Completely transparent")
                        continue
                
                # Check reasonable size
                if img.size[0] < 8 or img.size[1] < 8:
                    issues.append(f"⚠️  {sprite_file.name}: Very small ({img.size})")
                elif img.size[0] > 128 or img.size[1] > 128:
                    issues.append(f"⚠️  {sprite_file.name}: Very large ({img.size})")
                else:
                    good_sprites += 1
                    
        except Exception as e:
            issues.append(f"❌ {sprite_file.name}: Could not open - {e}")
    
    print(f"\n📊 Sprite Quality Check:")
    print(f"✅ Good sprites: {good_sprites}")
    print(f"⚠️  Issues found: {len(issues)}")
    
    if issues:
        print("\nIssues:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
    else:
        print("🎉 All sprites look good!")

def main():
    print("🎨 Testing generated sprites...")
    create_sprite_overview()

if __name__ == "__main__":
    main()