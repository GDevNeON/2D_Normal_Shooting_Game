"""
Game Modes Configuration

This module contains configuration and constants for game modes.
"""

# Game mode types
GAME_MODE_NORMAL = 1
GAME_MODE_ENDLESS = 0
GAME_MODE_CUSTOM = 2

# Custom game mode names
CUSTOM_MODE_ELITE_MADNESS = "elite_madness"
CUSTOM_MODE_TINY_SPEED_DEMON = "tiny_speed_demon"
CUSTOM_MODE_DOUBLE_BOZOS = "double_bozos"

# Default game mode settings
DEFAULT_GAME_MODES = [
    {
        "id": CUSTOM_MODE_ELITE_MADNESS,
        "name": "ELITE MADNESS",
        "description": "Spawn elite enemies every 15 seconds; recover max health, energy, EXP over time; NO LONGER SPAWN NORMAL ENEMIES AND BOSS.",
        "rules": {
            "player_damage_multiplier": 2.0,
            "enemy_elite_damage_multiplier": 2.0,
            "elite_spawn_interval": 15000,  # 15 seconds
            "elite_spawn_count": 3,
            "stat_recovery_interval": 1000,  # 10 seconds
            "disable_normal_enemies": True,
            "disable_boss": True
        }
    },
    {
        "id": CUSTOM_MODE_TINY_SPEED_DEMON,
        "name": "TINY SPEED DEMON",
        "description": "Player's size is tiny and move and shoot faster; enemies are also tiny and more aggressive.",
        "rules": {
            "player_speed_multiplier": 2.0,
            "player_size_multiplier": 0.5,
            "enemy_speed_multiplier": 1.8,
            "enemy_size_multiplier": 0.5,
            "boss_size_multiplier": 0.6,  # Boss will be 60% of original size
            "boss_speed_multiplier": 2,
            "bullet_speed_multiplier": 1.5,
            "enemy_spawn_interval": 3000,  # 3 seconds
            "elite_spawn_interval": 10000,  # 10 seconds
            "boss_spawn_interval": 300000,  # 5 minutes
            "disable_boss": False
        }
    },
    {
        "id": CUSTOM_MODE_DOUBLE_BOZOS,
        "name": "DOUBLE BOZOS",
        "description": "Encounter double bosses at start and items will randomly drop around player every second; NO LONGER SPAWN NORMAL AND ELITE ENEMIES.",
        "rules": {
            "initial_boss_count": 2,  # Number of bosses to spawn at start
            "item_drop_interval": 1000,  # 1 seconds
            "item_drop_count": 4,
            "disable_normal_enemies": True,
            "disable_elite_enemies": True,
            "boss_damage_multiplier": 1.0,  # Base damage multiplier
            "boss_speed_multiplier": 1.0,   # Base speed multiplier
            "boss_dash_speed_multiplier": 1.0,  # Base dash speed multiplier
            "player_health_multiplier": 1.5,  # Give player more health to compensate
            "max_wave_count": 5,  # Maximum number of waves (for stat scaling)
            "max_sprite_skills": 10,  # Maximum number of additional sprite skills
            "sprite_skills_per_wave": 2,  # Number of sprite skills to add per wave
            "boss_defeat_interval": 5000  # 5 seconds to next wave
        }
    }
]
