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
male_idle = [male_idle1, male_idle2]

male_run1               = "../../Sprites/Players/mc_run1.png"
male_run2               = "../../Sprites/Players/mc_run2.png"
male_run3               = "../../Sprites/Players/mc_run3.png"
male_run4               = "../../Sprites/Players/mc_run4.png"
male_run5               = "../../Sprites/Players/mc_run5.png"
male_run6               = "../../Sprites/Players/mc_run6.png"
male_run = [male_run1, male_run2, male_run3, male_run4, male_run5, male_run6]

female_idle1            = "../../Sprites/Players/fmc_idle1.png"
female_idle2            = "../../Sprites/Players/fmc_idle2.png"
female_idle = [female_idle1, female_idle2]

female_run1             = "../../Sprites/Players/fmc_run1.png"
female_run2             = "../../Sprites/Players/fmc_run2.png"
female_run3             = "../../Sprites/Players/fmc_run3.png"
female_run4             = "../../Sprites/Players/fmc_run4.png"
female_run5             = "../../Sprites/Players/fmc_run5.png"
female_run6             = "../../Sprites/Players/fmc_run6.png"
female_run = [female_run1, female_run2, female_run3, female_run4, female_run5, female_run6]

ghost1                  = "../../Sprites/Normal/ghost1.png"
ghost2                  = "../../Sprites/Normal/ghost2.png"
ghost = [ghost1, ghost2]

goblin1                  = "../../Sprites/Normal/goblin1.png"
goblin2                  = "../../Sprites/Normal/goblin2.png"
goblin = [goblin1, goblin2]

skeleton1                  = "../../Sprites/Normal/skeleton1.png"
skeleton2                  = "../../Sprites/Normal/skeleton2.png"
skeleton = [skeleton1, skeleton2]

slime1                  = "../../Sprites/Normal/slime1.png"
slime2                  = "../../Sprites/Normal/slime2.png"
slime = [slime1, slime2]

player_bullet           = "../../Sprites/Items/player_bullet.png"


background_sprite       = (mod_path / background1).resolve()
exp_sprite              = (mod_path / exp).resolve()
energy_sprite           = (mod_path / energy).resolve()
hp_sprite               = (mod_path / hp).resolve()

male_idle_sprite = []
for s in male_idle:
    sprite = (mod_path / s).resolve()
    image = pygame.image.load(sprite).convert()
    image.set_colorkey((0, 0, 0, 0), RLEACCEL)
    male_idle_sprite.append(image)

male_run_sprite = []
for s in male_run:
    sprite = (mod_path / s).resolve()
    image = pygame.image.load(sprite).convert()
    image.set_colorkey((0, 0, 0, 0), RLEACCEL)
    male_run_sprite.append(image)

female_idle_sprite = []
for s in female_idle:
    sprite = (mod_path / s).resolve()
    image = pygame.image.load(sprite).convert()
    image.set_colorkey((0, 0, 0, 0), RLEACCEL)
    female_idle_sprite.append(image)

female_run_sprite = []
for s in female_run:
    sprite = (mod_path / s).resolve()
    image = pygame.image.load(sprite).convert()
    image.set_colorkey((0, 0, 0, 0), RLEACCEL)
    female_run_sprite.append(image)

player_bullet_sprite    = (mod_path / player_bullet).resolve()

