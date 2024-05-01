from pathlib import Path

cwd = Path.cwd()

mod_path = Path(__file__).parent

grassplain_boss_path = "../../Sounds/BGM/grassplain_boss.mp3"
grassplain_boss = (mod_path / grassplain_boss_path).resolve()
grassplain_path = "../../Sounds/BGM/grassfield_bgm.mp3"
grassplain = (mod_path / grassplain_path).resolve()
menu_path = "../../Sounds/BGM/menu_bgm.mp3"
menu = (mod_path / menu_path).resolve()