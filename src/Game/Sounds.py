from pathlib import Path

cwd = Path.cwd()

mod_path = Path(__file__).parent

grassplain_boss_path = "../../Sounds/BGM/grassplain_boss.mp3"
grassplain_boss = (mod_path / grassplain_boss_path).resolve()

