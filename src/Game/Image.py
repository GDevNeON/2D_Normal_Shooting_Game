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

male_idle1              = "../../Sprites/Players/mc_idle1.png"
male_idle2              = "../../Sprites/Players/mc_idle2.png"
male_idle_path = [male_idle1, male_idle2]

male_run1               = "../../Sprites/Players/mc_run1.png"
male_run2               = "../../Sprites/Players/mc_run2.png"
male_run3               = "../../Sprites/Players/mc_run3.png"
male_run4               = "../../Sprites/Players/mc_run4.png"
male_run5               = "../../Sprites/Players/mc_run5.png"
male_run6               = "../../Sprites/Players/mc_run6.png"
male_run_path = [male_run1, male_run2, male_run3, male_run4, male_run5, male_run6]

female_idle1            = "../../Sprites/Players/fmc_idle1.png"
female_idle2            = "../../Sprites/Players/fmc_idle2.png"
female_idle_path = [female_idle1, female_idle2]

female_run1             = "../../Sprites/Players/fmc_run1.png"
female_run2             = "../../Sprites/Players/fmc_run2.png"
female_run3             = "../../Sprites/Players/fmc_run3.png"
female_run4             = "../../Sprites/Players/fmc_run4.png"
female_run5             = "../../Sprites/Players/fmc_run5.png"
female_run6             = "../../Sprites/Players/fmc_run6.png"
female_run_path = [female_run1, female_run2, female_run3, female_run4, female_run5, female_run6]

ghost1                  = "../../Sprites/Enemies/Normal/ghost1.png"
ghost2                  = "../../Sprites/Enemies/Normal/ghost2.png"
ghost_path = [ghost1, ghost2]

goblin1                 = "../../Sprites/Enemies/Normal/goblin1.png"
goblin2                 = "../../Sprites/Enemies/Normal/goblin2.png"
goblin_path = [goblin1, goblin2]

skeleton1               = "../../Sprites/Enemies/Normal/skeleton1.png"
skeleton2               = "../../Sprites/Enemies/Normal/skeleton2.png"
skeleton_path = [skeleton1, skeleton2]

slime1                  = "../../Sprites/Enemies/Normal/slime1.png"
slime2                  = "../../Sprites/Enemies/Normal/slime2.png"
slime_path = [slime1, slime2]

player_bullet           = "../../Sprites/Items/player_bullet.png"


# Image conversion
background_path         = (mod_path / background1).resolve()
exp_path                = (mod_path / exp).resolve()
energy_path             = (mod_path / energy).resolve()
hp_path                 = (mod_path / hp).resolve()

background_sprite       = pygame.image.load(background_path).convert()
exp_sprite              = pygame.image.load(exp_path).convert()
energy_sprite           = pygame.image.load(energy_path).convert()
hp_sprite               = pygame.image.load(hp_path).convert()

def convert_to_img(img_group_sprite, img_group_path):
    for s in img_group_path:
        sprite = (mod_path / s).resolve()
        image = pygame.image.load(sprite).convert()
        size = image.get_size()
        size_ratio = 2
        image = pygame.transform.scale(image, (int(size[0]/size_ratio), int(size[1]/size_ratio)))
        image.set_colorkey((0, 0, 0, 0), RLEACCEL)
        img_group_sprite.append(image)
        
# Player
player_bullet_path      = (mod_path / player_bullet).resolve()
player_bullet_sprite    = pygame.image.load(player_bullet_path).convert()

male_idle_sprite = []
convert_to_img(male_idle_sprite, male_idle_path)

male_run_sprite = []
convert_to_img(male_run_sprite, male_run_path)

female_idle_sprite = []
convert_to_img(female_idle_sprite, female_idle_path)

female_run_sprite = []
convert_to_img(female_run_sprite, female_run_path)
   
# Normal enemies 
ghost_sprite = []
convert_to_img(ghost_sprite, ghost_path)
    
goblin_sprite = []
convert_to_img(goblin_sprite, goblin_path)
    
skeleton_sprite = []
convert_to_img(skeleton_sprite, skeleton_path)
    
slime_sprite = []
convert_to_img(slime_sprite, slime_path)
