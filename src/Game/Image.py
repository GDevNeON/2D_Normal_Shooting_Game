import pygame
from DEFINE import *
from pathlib import Path

cwd = Path.cwd()

mod_path = Path(__file__).parent

background1             = "../../Sprites/Backgrounds/grassplain.png"
background2             = "../../Sprites/Backgrounds/grassplain.png"
exp                     = "../../Sprites/Items/exp_item.png"
energy                  = "../../Sprites/Items/energy_item.png"
hp                      = "../../Sprites/Items/hp_item.png"

male_damaged            = "../../Sprites/Players/mc_damaged.png"
male_idle1              = "../../Sprites/Players/mc_idle1.png"
male_idle2              = "../../Sprites/Players/mc_idle2.png"
male_idle_path          = [male_idle1, male_idle2]

male_run1               = "../../Sprites/Players/mc_run1.png"
male_run2               = "../../Sprites/Players/mc_run2.png"
male_run3               = "../../Sprites/Players/mc_run3.png"
male_run4               = "../../Sprites/Players/mc_run4.png"
male_run5               = "../../Sprites/Players/mc_run5.png"
male_run6               = "../../Sprites/Players/mc_run6.png"
male_run_path           = [male_run1, male_run2, male_run3, male_run4, male_run5, male_run6]

female_damaged          = "../../Sprites/Players/fmc_damaged.png"
female_idle1            = "../../Sprites/Players/fmc_idle1.png"
female_idle2            = "../../Sprites/Players/fmc_idle2.png"
female_idle_path        = [female_idle1, female_idle2]

female_run1             = "../../Sprites/Players/fmc_run1.png"
female_run2             = "../../Sprites/Players/fmc_run2.png"
female_run3             = "../../Sprites/Players/fmc_run3.png"
female_run4             = "../../Sprites/Players/fmc_run4.png"
female_run5             = "../../Sprites/Players/fmc_run5.png"
female_run6             = "../../Sprites/Players/fmc_run6.png"
female_run_path         = [female_run1, female_run2, female_run3, female_run4, female_run5, female_run6]

player_bullet           = "../../Sprites/Items/player_bullet.png"

ghost_damaged           = "../../Sprites/Players/ghost_damaged.png"
ghost1                  = "../../Sprites/Enemies/Normal/ghost1.png"
ghost2                  = "../../Sprites/Enemies/Normal/ghost2.png"
ghost_path              = [ghost1, ghost2]

goblin_damaged          = "../../Sprites/Players/goblin_damaged.png"
goblin1                 = "../../Sprites/Enemies/Normal/goblin1.png"
goblin2                 = "../../Sprites/Enemies/Normal/goblin2.png"
goblin_path             = [goblin1, goblin2]

skeleton_damaged        = "../../Sprites/Players/skeleton_damaged.png"
skeleton1               = "../../Sprites/Enemies/Normal/skeleton1.png"
skeleton2               = "../../Sprites/Enemies/Normal/skeleton2.png"
skeleton_path           = [skeleton1, skeleton2]

slime_damaged           = "../../Sprites/Players/slime_damaged.png"
slime1                  = "../../Sprites/Enemies/Normal/slime1.png"
slime2                  = "../../Sprites/Enemies/Normal/slime2.png"
slime_path              = [slime1, slime2]

eghost_damaged          = "../../Sprites/Players/eghost_damaged.png"
eghost1                 = "../../Sprites/Enemies/Elite/eghost1.png"
eghost2                 = "../../Sprites/Enemies/Elite/eghost2.png"
eghost_path             = [eghost1, eghost2]

egoblin_damaged         = "../../Sprites/Players/egoblin_damaged.png"
egoblin1                = "../../Sprites/Enemies/Elite/egoblin1.png"
egoblin2                = "../../Sprites/Enemies/Elite/egoblin2.png"
egoblin_path            = [egoblin1, egoblin2]

eskeleton_damaged       = "../../Sprites/Players/eskeleton_damaged.png"
eskeleton1              = "../../Sprites/Enemies/Elite/eskeleton1.png"
eskeleton2              = "../../Sprites/Enemies/Elite/eskeleton2.png"
eskeleton_path          = [eskeleton1, eskeleton2]

eslime_damaged          = "../../Sprites/Players/eslime_damaged.png"
eslime1                 = "../../Sprites/Enemies/Elite/eslime1.png"
eslime2                 = "../../Sprites/Enemies/Elite/eslime2.png"
eslime_path             = [eslime1, eslime2]

skelly_walk1            = "../../Sprites/Enemies/Boss/skelly_walk1.png"
skelly_walk2            = "../../Sprites/Enemies/Boss/skelly_walk2.png"
skelly_walk_path        = [skelly_walk1, skelly_walk2]
skellyphase2_walk1      = "../../Sprites/Enemies/Boss/skellyphase2_walk1.png"
skellyphase2_walk2      = "../../Sprites/Enemies/Boss/skellyphase2_walk2.png"
skellyphase2_walk_path  = [skellyphase2_walk1, skellyphase2_walk2]

skelly_1st_skill1       = "../../Sprites/Enemies/Boss/skelly_1st_skill1.png"
skelly_1st_skill2       = "../../Sprites/Enemies/Boss/skelly_1st_skill2.png"
skelly_1st_skill_path   = [skelly_1st_skill1, skelly_1st_skill2]
swordskill1             = "../../Sprites/Enemies/Boss/swordskill1.png"
swordskill2             = "../../Sprites/Enemies/Boss/swordskill2.png"
swordskill3             = "../../Sprites/Enemies/Boss/swordskill3.png"
swordskill4             = "../../Sprites/Enemies/Boss/swordskill4.png"
swordskill5             = "../../Sprites/Enemies/Boss/swordskill5.png"
swordskill_path         = [swordskill1, swordskill2, swordskill3, swordskill4, swordskill5]

skelly_2nd_skill1       = "../../Sprites/Enemies/Boss/skelly_2nd_skill1.png"
skelly_2nd_skill2       = "../../Sprites/Enemies/Boss/skelly_2nd_skill2.png"
skelly_2nd_skill_path   = [skelly_2nd_skill1, skelly_2nd_skill2]
swordcast1              = "../../Sprites/Enemies/Boss/swordcast1.png"
swordcast2              = "../../Sprites/Enemies/Boss/swordcast2.png"
swordcast3              = "../../Sprites/Enemies/Boss/swordcast3.png"
swordcast4              = "../../Sprites/Enemies/Boss/swordcast4.png"
swordcast_path          = [swordcast1, swordcast2, swordcast3, swordcast4]

skele_phasetrans1       = "../../Sprites/Enemies/Boss/skele_phasetrans1.png"
skele_phasetrans2       = "../../Sprites/Enemies/Boss/skele_phasetrans2.png"
skele_phasetrans_path   = [skele_phasetrans1, skelly_walk2]

skelly_atk              = "../../Sprites/Enemies/Boss/skelly_atk.png"
skellyphase2_atk        = "../../Sprites/Enemies/Boss/skellyphase2_atk.png"
skelly_damaged          = "../../Sprites/Enemies/Boss/skelly_damaged.png"
skelly_feather          = "../../Sprites/Enemies/Boss/skelly_feather.png"

warning            = "../../Sprites/Backgrounds/warning.png"

# Image conversion
def change_color(image, color):
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

def convert_to_img(img_group_sprite, img_group_path, size_ratio):
    for s in img_group_path:
        sprite = (mod_path / s).resolve()
        image = pygame.image.load(sprite).convert_alpha()
        size = image.get_size()
        image = pygame.transform.scale(image, (int(size[0]/size_ratio), int(size[1]/size_ratio)))
        image.set_colorkey((0, 0, 0, 0), RLEACCEL)
        img_group_sprite.append(image)
        
background_path         = (mod_path / background1).resolve()
exp_path                = (mod_path / exp).resolve()
energy_path             = (mod_path / energy).resolve()
hp_path                 = (mod_path / hp).resolve()

background_sprite       = pygame.image.load(background_path).convert()
exp_sprite              = pygame.image.load(exp_path).convert()
energy_sprite           = pygame.image.load(energy_path).convert()
hp_sprite               = pygame.image.load(hp_path).convert()
      
# Player
player_bullet_path      = (mod_path / player_bullet).resolve()
player_bullet_sprite    = pygame.image.load(player_bullet_path).convert()

player_bullet_path      = (mod_path / player_bullet).resolve()
player_bullet_sprite    = pygame.image.load(player_bullet_path).convert()

male_damaged_path       = (mod_path / male_damaged).resolve()
male_damaged_sprite     = pygame.image.load(male_damaged_path).convert()

male_idle_sprite = []
convert_to_img(male_idle_sprite, male_idle_path, 1.5)

male_run_sprite = []
convert_to_img(male_run_sprite, male_run_path, 1.5)

female_damaged_path      = (mod_path / female_damaged).resolve()
female_damaged_sprite    = pygame.image.load(female_damaged_path).convert()

female_idle_sprite = []
convert_to_img(female_idle_sprite, female_idle_path, 1.5)

female_run_sprite = []
convert_to_img(female_run_sprite, female_run_path, 1.5)
   
# Normal enemies 
ghost_sprite = []
convert_to_img(ghost_sprite, ghost_path, 10)
    
goblin_sprite = []
convert_to_img(goblin_sprite, goblin_path, 10)
    
skeleton_sprite = []
convert_to_img(skeleton_sprite, skeleton_path, 2.5)
    
slime_sprite = []
convert_to_img(slime_sprite, slime_path, 2)

# Elite enemies
eghost_sprite = []
convert_to_img(eghost_sprite, eghost_path, 1)

egoblin_sprite = []
convert_to_img(egoblin_sprite, egoblin_path, 1)

eskeleton_sprite = []
convert_to_img(eskeleton_sprite, eskeleton_path, 1)

eslime_sprite = []
convert_to_img(eslime_sprite, eslime_path, 1)

# Boss enemies
skelly_atk_path      = (mod_path / skelly_atk).resolve()
skelly_atk_sprite    = pygame.image.load(skelly_atk_path).convert()

skellyphase2_atk_path      = (mod_path / skellyphase2_atk).resolve()
skellyphase2_atk_sprite    = pygame.image.load(skellyphase2_atk_path).convert()

skelly_damaged_path      = (mod_path / skelly_damaged).resolve()
skelly_damaged_sprite    = pygame.image.load(skelly_damaged_path).convert()

skelly_feather_path      = (mod_path / skelly_feather).resolve()
skelly_feather_sprite    = pygame.image.load(skelly_feather_path).convert()

skelly_walk_sprite = []
convert_to_img(skelly_walk_sprite, skelly_walk_path, 1)

skellyphase2_walk_sprite = []
convert_to_img(skellyphase2_walk_sprite, skellyphase2_walk_path, 1)

skelly_1st_skill_sprite = []
convert_to_img(skelly_1st_skill_sprite, skelly_1st_skill_path, 1)

skelly_swordskill_sprite = []
convert_to_img(skelly_swordskill_sprite, swordskill_path, 1)

skelly_2nd_skill_sprite = []
convert_to_img(skelly_2nd_skill_sprite, skelly_2nd_skill_path, 1)

skelly_swordcast_sprite = []
convert_to_img(skelly_swordcast_sprite, swordcast_path, 1)

skelly_phasetrans_sprite = []
convert_to_img(skelly_phasetrans_sprite, skele_phasetrans_path, 1)

warning_path      = (mod_path / warning).resolve()
warning_sprite    = pygame.image.load(warning_path).convert_alpha()
    