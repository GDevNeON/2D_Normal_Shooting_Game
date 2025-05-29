import pygame
from ..core.define import *
from pathlib import Path

# Size constants
BOSS_SIZE = 1.5  # Scale factor for boss sprites

# Get current working directory and module path
cwd = Path.cwd()
mod_path = Path(__file__).parent.parent

# Asset paths
background1             = "assets/sprites/backgrounds/grassplain.png"
background2             = "assets/sprites/backgrounds/grassplain.png"
exp                     = "assets/sprites/items/exp_item.png"
energy                  = "assets/sprites/items/energy_item.png"
hp                      = "assets/sprites/items/hp_item.png"

male_damaged            = "assets/sprites/players/mc_damaged.png"
male_idle1              = "assets/sprites/players/mc_idle1.png"
male_idle2              = "assets/sprites/players/mc_idle2.png"
male_idle_path          = [male_idle1, male_idle2]

male_run1               = "assets/sprites/players/mc_run1.png"
male_run2               = "assets/sprites/players/mc_run2.png"
male_run3               = "assets/sprites/players/mc_run3.png"
male_run4               = "assets/sprites/players/mc_run4.png"
male_run5               = "assets/sprites/players/mc_run5.png"
male_run6               = "assets/sprites/players/mc_run6.png"
male_run_path           = [male_run1, male_run2, male_run3, male_run4, male_run5, male_run6]

female_damaged          = "assets/sprites/players/fmc_damaged.png"
female_idle1            = "assets/sprites/players/fmc_idle1.png"
female_idle2            = "assets/sprites/players/fmc_idle2.png"
female_idle_path        = [female_idle1, female_idle2]

female_run1             = "assets/sprites/players/fmc_run1.png"
female_run2             = "assets/sprites/players/fmc_run2.png"
female_run3             = "assets/sprites/players/fmc_run3.png"
female_run4             = "assets/sprites/players/fmc_run4.png"
female_run5             = "assets/sprites/players/fmc_run5.png"
female_run6             = "assets/sprites/players/fmc_run6.png"
female_run_path         = [female_run1, female_run2, female_run3, female_run4, female_run5, female_run6]

player_bullet           = "assets/sprites/items/player_bullet.png"
burst_bullet            = "assets/sprites/items/burst_bullet.png"
laser_bullet            = "assets/sprites/items/laser_bullet.png"

ghost_damaged           = "assets/sprites/players/ghost_damaged.png"
ghost1                  = "assets/sprites/enemies/normal/ghost1.png"
ghost2                  = "assets/sprites/enemies/normal/ghost2.png"
ghost_path              = [ghost1, ghost2]

goblin_damaged          = "assets/sprites/players/goblin_damaged.png"
goblin1                 = "assets/sprites/enemies/normal/goblin1.png"
goblin2                 = "assets/sprites/enemies/normal/goblin2.png"
goblin_path             = [goblin1, goblin2]

skeleton_damaged        = "assets/sprites/players/skeleton_damaged.png"
skeleton1               = "assets/sprites/enemies/normal/skeleton1.png"
skeleton2               = "assets/sprites/enemies/normal/skeleton2.png"
skeleton_path           = [skeleton1, skeleton2]

slime_damaged           = "assets/sprites/players/slime_damaged.png"
slime1                  = "assets/sprites/enemies/normal/slime1.png"
slime2                  = "assets/sprites/enemies/normal/slime2.png"
slime_path              = [slime1, slime2]

eghost_damaged          = "assets/sprites/players/eghost_damaged.png"
eghost1                 = "assets/sprites/enemies/elite/eghost1.png"
eghost2                 = "assets/sprites/enemies/elite/eghost2.png"
eghost_path             = [eghost1, eghost2]

egoblin_damaged         = "assets/sprites/players/egoblin_damaged.png"
egoblin1                = "assets/sprites/enemies/elite/egoblin1.png"
egoblin2                = "assets/sprites/enemies/elite/egoblin2.png"
egoblin_path            = [egoblin1, egoblin2]

eskeleton_damaged       = "assets/sprites/players/eskeleton_damaged.png"
eskeleton1              = "assets/sprites/enemies/elite/eskeleton1.png"
eskeleton2              = "assets/sprites/enemies/elite/eskeleton2.png"
eskeleton_path          = [eskeleton1, eskeleton2]

eslime_damaged          = "assets/sprites/players/eslime_damaged.png"
eslime1                 = "assets/sprites/enemies/elite/eslime1.png"
eslime2                 = "assets/sprites/enemies/elite/eslime2.png"
eslime_path             = [eslime1, eslime2]

skelly_walk1            = "assets/sprites/enemies/boss/skelly_walk1.png"
skelly_walk2            = "assets/sprites/enemies/boss/skelly_walk2.png"
skelly_walk_path        = [skelly_walk1, skelly_walk2]
skellyphase2_walk1      = "assets/sprites/enemies/boss/skellyphase2_walk1.png"
skellyphase2_walk2      = "assets/sprites/enemies/boss/skellyphase2_walk2.png"
skellyphase2_walk_path  = [skellyphase2_walk1, skellyphase2_walk2]

skelly_1st_skill1       = "assets/sprites/enemies/boss/skelly_1st_skill1.png"
skelly_1st_skill2       = "assets/sprites/enemies/boss/skelly_1st_skill2.png"
skelly_1st_skill_path   = [skelly_1st_skill1, skelly_1st_skill2]
swordskill1             = "assets/sprites/enemies/boss/swordskill1.png"
swordskill2             = "assets/sprites/enemies/boss/swordskill2.png"
swordskill3             = "assets/sprites/enemies/boss/swordskill3.png"
swordskill4             = "assets/sprites/enemies/boss/swordskill4.png"
swordskill5             = "assets/sprites/enemies/boss/swordskill5.png"
swordskill_path         = [swordskill1, swordskill2, swordskill3, swordskill4, swordskill5]

skelly_2nd_skill1       = "assets/sprites/enemies/boss/skelly_2nd_skill1.png"
skelly_2nd_skill2       = "assets/sprites/enemies/boss/skelly_2nd_skill2.png"
skelly_2nd_skill_path   = [skelly_2nd_skill1, skelly_2nd_skill2]
swordcast1              = "assets/sprites/enemies/boss/swordcast1.png"
swordcast2              = "assets/sprites/enemies/boss/swordcast2.png"
swordcast3              = "assets/sprites/enemies/boss/swordcast3.png"
swordcast4              = "assets/sprites/enemies/boss/swordcast4.png"
swordcast_path          = [swordcast1, swordcast2, swordcast3, swordcast4]

skele_phasetrans1       = "assets/sprites/enemies/boss/skele_phasetrans1.png"
skele_phasetrans2       = "assets/sprites/enemies/boss/skele_phasetrans2.png"
skele_phasetrans_path   = [skele_phasetrans1, skele_phasetrans2]

skelly_atk              = "assets/sprites/enemies/boss/skelly_atk.png"
skellyphase2_atk        = "assets/sprites/enemies/boss/skellyphase2_atk.png"
skelly_damaged          = "assets/sprites/enemies/boss/skelly_damaged.png"
skelly_feather          = "assets/sprites/enemies/boss/skelly_feather.png"

warning                 = "assets/sprites/backgrounds/warning.png"

# Image conversion functions
def change_color(image, color):
    """Change the color of non-transparent pixels in an image"""
    # Create a copy of the surface
    new_surface = image.copy()
    # Iterate through each pixel of the surface
    for x in range(new_surface.get_width()):
        for y in range(new_surface.get_height()):
            # Get the color of the pixel at (x, y)
            pixel_color = new_surface.get_at((x, y))
            # Check if the pixel is not transparent (alpha value != 0)
            if pixel_color.a != 0:
                # Replace the pixel color with the new color
                new_surface.set_at((x, y), color)
    # Return the new surface
    return new_surface

def scale_to_size(image, target_size):
    """Scale image to target size while maintaining aspect ratio"""
    # Calculate the scaling factor while maintaining aspect ratio
    width_ratio = target_size[0] / image.get_width()
    height_ratio = target_size[1] / image.get_height()
    scale = min(width_ratio, height_ratio)
    
    # Calculate new dimensions
    new_width = int(image.get_width() * scale)
    new_height = int(image.get_height() * scale)
    
    # Create a new surface with target size and transparent background
    new_surface = pygame.Surface(target_size, pygame.SRCALPHA)
    
    # Calculate position to center the scaled image
    x = (target_size[0] - new_width) // 2
    y = (target_size[1] - new_height) // 2
    
    # Scale and blit the image onto the new surface
    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    new_surface.blit(scaled_image, (x, y))
    
    return new_surface

def convert_to_img(img_group_sprite, img_group_path, enemy_type="normal"):
    """
    Convert image paths to pygame surfaces and add to sprite list
    
    Args:
        img_group_sprite: List to store the loaded sprites
        img_group_path: List of paths to the sprite images
        enemy_type: Type of enemy ("normal", "elite", "boss")
    """
    print(f"Starting to load {len(img_group_path)} {enemy_type} sprites...")
    
    # Define target sizes for different enemy types
    TARGET_SIZES = {
        "normal": (64, 64),
        "elite": (96, 96),  # 1.5x normal size
        "boss": (192, 192)  # 3x normal size
    }
    
    target_size = TARGET_SIZES.get(enemy_type, (64, 64))
    
    for i, sprite in enumerate(img_group_path):
        try:
            path = (mod_path / sprite).resolve()
            print(f"Loading {enemy_type} sprite {i+1}: {path}")
            if not path.exists():
                print(f"  Error: File not found: {path}")
                continue
                
            # Load the image with alpha channel
            image = pygame.image.load(str(path)).convert_alpha()
            if image is None:
                print(f"  Error: Failed to load image: {path}")
                continue
            
            # Scale the image to target size while maintaining aspect ratio
            scaled_image = scale_to_size(image, target_size)
            
            # If the image has no alpha channel, set black as colorkey
            if scaled_image.get_alpha() is None:
                scaled_image = scaled_image.convert()
                scaled_image.set_colorkey((0, 0, 0))
            
            img_group_sprite.append(scaled_image)
            print(f"  Successfully loaded and scaled to {target_size[0]}x{target_size[1]}")
            
        except Exception as e:
            print(f"  Error loading image {sprite}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"Finished loading {len(img_group_sprite)}/{len(img_group_path)} {enemy_type} sprites")
        
# Load background and item sprites
background_path         = (mod_path / background1).resolve()
exp_path                = (mod_path / exp).resolve()
energy_path             = (mod_path / energy).resolve()
hp_path                 = (mod_path / hp).resolve()

background_sprite       = pygame.image.load(background_path).convert()
exp_sprite              = pygame.image.load(exp_path).convert()
energy_sprite           = pygame.image.load(energy_path).convert()
hp_sprite               = pygame.image.load(hp_path).convert()
      
# Player bullet sprites
player_bullet_path      = (mod_path / player_bullet).resolve()
player_bullet_sprite    = pygame.image.load(player_bullet_path).convert()

burst_bullet_path       = (mod_path / burst_bullet).resolve()
burst_bullet_sprite     = pygame.image.load(burst_bullet_path).convert() if Path(burst_bullet_path).exists() else player_bullet_sprite

laser_bullet_path       = (mod_path / laser_bullet).resolve()
laser_bullet_sprite     = pygame.image.load(laser_bullet_path).convert() if Path(laser_bullet_path).exists() else player_bullet_sprite

# Player damaged sprites
male_damaged_path       = (mod_path / male_damaged).resolve()
male_damaged_sprite     = pygame.image.load(male_damaged_path).convert()

female_damaged_path     = (mod_path / female_damaged).resolve()
female_damaged_sprite   = pygame.image.load(female_damaged_path).convert()

# Player animation sprites
male_idle_sprite = []
convert_to_img(male_idle_sprite, male_idle_path, 0.8)

male_run_sprite = []
convert_to_img(male_run_sprite, male_run_path, 0.8)

female_idle_sprite = []
convert_to_img(female_idle_sprite, female_idle_path, 0.8)

female_run_sprite = []
convert_to_img(female_run_sprite, female_run_path, 0.8)

# Flipped player sprites for facing left
male_idle_sprite_left = [pygame.transform.flip(sprite, True, False) for sprite in male_idle_sprite]
male_run_sprite_left = [pygame.transform.flip(sprite, True, False) for sprite in male_run_sprite]
female_idle_sprite_left = [pygame.transform.flip(sprite, True, False) for sprite in female_idle_sprite]
female_run_sprite_left = [pygame.transform.flip(sprite, True, False) for sprite in female_run_sprite]
   
# Normal enemies - using standard 64x64 size
ghost_sprite = []
convert_to_img(ghost_sprite, ghost_path, "normal")
    
goblin_sprite = []
convert_to_img(goblin_sprite, goblin_path, "normal")
    
skeleton_sprite = []
convert_to_img(skeleton_sprite, skeleton_path, "normal")
    
slime_sprite = []
convert_to_img(slime_sprite, slime_path, "normal")

# Elite enemies - using 1.5x size (96x96)
eghost_sprite = []
convert_to_img(eghost_sprite, eghost_path, "elite")

egoblin_sprite = []
convert_to_img(egoblin_sprite, egoblin_path, "elite")

eskeleton_sprite = []
convert_to_img(eskeleton_sprite, eskeleton_path, "elite")

eslime_sprite = []
convert_to_img(eslime_sprite, eslime_path, "elite")

def load_boss_sprites():
    """Load all boss sprites with error handling"""
    global skelly_walk_sprite, skellyphase2_walk_sprite, skelly_skill_sprite, skelly_transform_sprite
    
    print(f"Loading boss sprites with size ratio: {BOSS_SIZE}...")
    
    # Phase 1 walk sprites
    skelly_walk_sprite = []
    try:
        convert_to_img(skelly_walk_sprite, skelly_walk_path, BOSS_SIZE)
        print(f"Loaded {len(skelly_walk_sprite)} phase 1 walk sprites")
    except Exception as e:
        print(f"Error loading phase 1 walk sprites: {e}")
    
    # Phase 2 walk sprites
    skellyphase2_walk_sprite = []
    try:
        convert_to_img(skellyphase2_walk_sprite, skellyphase2_walk_path, BOSS_SIZE)
        print(f"Loaded {len(skellyphase2_walk_sprite)} phase 2 walk sprites")
    except Exception as e:
        print(f"Error loading phase 2 walk sprites: {e}")
    
    # Skill sprites
    skelly_skill_sprite = []
    try:
        convert_to_img(skelly_skill_sprite, skelly_1st_skill_path, BOSS_SIZE)
        print(f"Loaded {len(skelly_skill_sprite)} skill sprites")
    except Exception as e:
        print(f"Error loading skill sprites: {e}")
    
    # Transform sprites
    skelly_transform_sprite = []
    try:
        convert_to_img(skelly_transform_sprite, skele_phasetrans_path, BOSS_SIZE)
        print(f"Loaded {len(skelly_transform_sprite)} transform sprites")
    except Exception as e:
        print(f"Error loading transform sprites: {e}")

# Load boss sprites when the module is imported
load_boss_sprites()

# Load other boss-related sprites with consistent size
skelly_swordskill_sprite = []
convert_to_img(skelly_swordskill_sprite, swordskill_path, BOSS_SIZE)

skelly_swordcast_sprite = []
convert_to_img(skelly_swordcast_sprite, swordcast_path, BOSS_SIZE)

# Load boss attack sprites
skelly_atk_path = (mod_path / skelly_atk).resolve()
skelly_atk_sprite = None
skellyphase2_atk_sprite = None

try:
    skelly_atk_path_full = (mod_path / skelly_atk).resolve()
    if skelly_atk_path_full.exists():
        print(f"Loading phase 1 attack sprite: {skelly_atk}")
        skelly_atk_sprite = pygame.image.load(str(skelly_atk_path_full)).convert_alpha()
        skelly_atk_sprite = pygame.transform.scale_by(skelly_atk_sprite, BOSS_SIZE)
        print(f"Scaled phase 1 attack sprite by {BOSS_SIZE}x")
    else:
        print(f"Warning: Phase 1 attack sprite not found at {skelly_atk_path_full}")
        # Use a placeholder if needed
        if skelly_walk_sprite and len(skelly_walk_sprite) > 0:
            skelly_atk_sprite = pygame.transform.scale_by(skelly_walk_sprite[0].copy(), BOSS_SIZE)
        else:
            # Create a placeholder surface and scale it
            skelly_atk_sprite = pygame.Surface((int(80 * BOSS_SIZE), int(80 * BOSS_SIZE)), pygame.SRCALPHA)
            pygame.draw.rect(skelly_atk_sprite, (255, 0, 0), (0, 0, 80 * BOSS_SIZE, 80 * BOSS_SIZE))
            print("Created placeholder for phase 1 attack sprite")
except Exception as e:
    print(f"Error loading phase 1 attack sprite: {e}")
    # Create a placeholder surface with scaling
    skelly_atk_sprite = pygame.Surface((int(80 * BOSS_SIZE), int(80 * BOSS_SIZE)), pygame.SRCALPHA)
    pygame.draw.rect(skelly_atk_sprite, (255, 0, 0), (0, 0, 80 * BOSS_SIZE, 80 * BOSS_SIZE))

try:
    skellyphase2_atk_path_full = (mod_path / skellyphase2_atk).resolve()
    if skellyphase2_atk_path_full.exists():
        print(f"Loading phase 2 attack sprite: {skellyphase2_atk}")
        skellyphase2_atk_sprite = pygame.image.load(str(skellyphase2_atk_path_full)).convert_alpha()
        skellyphase2_atk_sprite = pygame.transform.scale_by(skellyphase2_atk_sprite, BOSS_SIZE)
        print(f"Scaled phase 2 attack sprite by {BOSS_SIZE}x")
    else:
        print(f"Warning: Phase 2 attack sprite not found at {skellyphase2_atk_path_full}")
        # Use a placeholder if needed
        if skellyphase2_walk_sprite and len(skellyphase2_walk_sprite) > 0:
            skellyphase2_atk_sprite = pygame.transform.scale_by(skellyphase2_walk_sprite[0].copy(), BOSS_SIZE)
        else:
            # Create a placeholder surface and scale it
            skellyphase2_atk_sprite = pygame.Surface((int(80 * BOSS_SIZE), int(80 * BOSS_SIZE)), pygame.SRCALPHA)
            pygame.draw.rect(skellyphase2_atk_sprite, (0, 0, 255), (0, 0, 80 * BOSS_SIZE, 80 * BOSS_SIZE))
            print("Created placeholder for phase 2 attack sprite")
except Exception as e:
    print(f"Error loading phase 2 attack sprite: {e}")
    # Create a placeholder surface with scaling
    skellyphase2_atk_sprite = pygame.Surface((int(80 * BOSS_SIZE), int(80 * BOSS_SIZE)), pygame.SRCALPHA)
    pygame.draw.rect(skellyphase2_atk_sprite, (0, 0, 255), (0, 0, 80 * BOSS_SIZE, 80 * BOSS_SIZE))

# Global variable to track if feather sprite is already loaded
_feather_loaded = False

def load_feather_sprite():
    """Load the feather sprite with error handling and scaling"""
    global skelly_feather_sprite, _feather_loaded
    
    # Only load once
    if _feather_loaded and skelly_feather_sprite is not None:
        print("[ImageManager] Using cached feather sprite")
        return
        
    try:
        feather_path = (mod_path / skelly_feather).resolve()
        print(f"[ImageManager] Loading feather sprite from: {feather_path}")
        
        if not feather_path.exists():
            error_msg = f"Feather sprite not found at {feather_path}"
            print(f"[ImageManager] Error: {error_msg}")
            raise FileNotFoundError(error_msg)
            
        # Load and scale the feather sprite
        feather_img = pygame.image.load(str(feather_path)).convert_alpha()
        skelly_feather_sprite = pygame.transform.scale(feather_img, (40, 40))
        _feather_loaded = True
        print(f"[ImageManager] Successfully loaded feather sprite. Size: {skelly_feather_sprite.get_size()}")
        
    except Exception as e:
        print(f"[ImageManager] Error loading feather sprite: {e}")
        # Create a placeholder sprite
        skelly_feather_sprite = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(skelly_feather_sprite, (255, 255, 0), (20, 20), 15)  # Yellow circle
        pygame.draw.circle(skelly_feather_sprite, (200, 200, 0), (20, 20), 10)  # Darker center
        _feather_loaded = True
        print("[ImageManager] Created placeholder feather sprite")

# Load boss damaged sprite
try:
    skelly_damaged_path = (mod_path / skelly_damaged).resolve()
    if skelly_damaged_path.exists():
        skelly_damaged_sprite = pygame.image.load(skelly_damaged_path).convert_alpha()
        # Scale the damaged sprite to match other boss sprites
        skelly_damaged_sprite = pygame.transform.scale_by(skelly_damaged_sprite, BOSS_SIZE)
        print(f"Loaded and scaled damaged sprite by {BOSS_SIZE}x: {skelly_damaged_path}")
    else:
        print(f"Warning: Damaged sprite not found at {skelly_damaged_path}")
        skelly_damaged_sprite = pygame.transform.scale_by(skelly_walk_sprite[0].copy(), BOSS_SIZE) if skelly_walk_sprite else None
        
    # Load feather sprite with scaling
    load_feather_sprite()
    
    # Warning sprite - scale to match the game's visual style
    warning_path = (mod_path / warning).resolve()
    if warning_path.exists():
        warning_sprite = pygame.image.load(warning_path).convert_alpha()
        # Scale warning sprite proportionally to BOSS_SIZE
        warning_sprite = pygame.transform.scale_by(warning_sprite, BOSS_SIZE * 0.5)  # Adjust scale factor as needed
        print(f"Loaded and scaled warning sprite: {warning_path}")
    else:
        warning_sprite = None
        
except Exception as e:
    print(f"Error loading sprites: {e}")
    # Ensure we have at least placeholder sprites with proper scaling
    if 'skelly_damaged_sprite' not in locals():
        skelly_damaged_sprite = pygame.Surface((int(80 * BOSS_SIZE), int(80 * BOSS_SIZE)), pygame.SRCALPHA)
        pygame.draw.rect(skelly_damaged_sprite, (255, 0, 0), (0, 0, 80 * BOSS_SIZE, 80 * BOSS_SIZE))
    if 'skelly_feather_sprite' not in globals():
        feather_size = int(40 * BOSS_SIZE * 0.5)  # Scale feather size relative to boss size
        skelly_feather_sprite = pygame.Surface((feather_size, feather_size), pygame.SRCALPHA)
        pygame.draw.circle(skelly_feather_sprite, (255, 200, 0), 
                          (feather_size//2, feather_size//2), feather_size//2)
