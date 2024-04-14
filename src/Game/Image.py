from pathlib import Path

cwd = Path.cwd()

mod_path = Path(__file__).parent

background      = "../../Sprites/Backgrounds/dungeon.png"
exp             = "../../Sprites/Players/exp_item.png"
energy          = "../../Sprites/Players/energy_item.png"
hp              = "../../Sprites/Players/hp_item.png"
player_bullet   = "../../Sprites/Players/player_bullet.png"

background_sprite       = (mod_path / background).resolve()
exp_sprite              = (mod_path / exp).resolve()
energy_sprite           = (mod_path / energy).resolve()
hp_sprite               = (mod_path / hp).resolve()
player_bullet_sprite    = (mod_path / player_bullet).resolve()