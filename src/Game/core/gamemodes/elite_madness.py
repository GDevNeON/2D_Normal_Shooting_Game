import random
import pygame
from . import BaseGameMode, register_game_mode
from ..define import ADD_ELITE, INCREASE_STAT, ADD_ENEMY, ADD_BOSS

@register_game_mode
class EliteMadnessMode(BaseGameMode):
    """ELITE MADNESS game mode - Spawn elite enemies frequently with enhanced stats."""
    
    def __init__(self):
        super().__init__(
            name="ELITE MADNESS",
            description="Spawn elite enemies every 15 seconds; recover max health, energy, current_exp over time; NO LONGER SPAWN NORMAL ENEMIES AND BOSS."
        )
        self.rules = {
            "player_damage_multiplier": 2.0,
            "enemy_elite_damage_multiplier": 2.0,
            "elite_spawn_interval": 15000,  # 15 seconds
            "elite_spawn_timer": 0,
            "stat_recovery_interval": 1000,  # 1 second
            "stat_recovery_timer": 500,
            "elite_spawn_count": 3,  # Number of elites to spawn per interval
            "elite_types": ["elite1", "elite2", "elite3", "elite4"],
            "elite_weights": [0.4, 0.3, 0.2, 0.1],  # Weighted random for elite types
            "disable_normal_enemies": True,
            "disable_boss": True
        }
        self.is_endless = True
    
    def setup(self, game_state):
        """Initialize the ELITE MADNESS game mode."""
        # Disable normal enemy and boss spawns
        pygame.time.set_timer(ADD_ENEMY, 0)
        pygame.time.set_timer(ADD_BOSS, 0)
        
        # Set up elite spawn timer
        self.rules["elite_spawn_timer"] = pygame.time.get_ticks()
        self.rules["stat_recovery_timer"] = pygame.time.get_ticks()
        
        # Apply player buffs
        player = game_state.get('player')
        if player:
            # Instead of using damage_multiplier, modify damage_buff
            # This will affect bullet damage calculation
            player.damage_buff = (self.rules["player_damage_multiplier"] - 1) * 100  # Convert to percentage
            print(f"[ELITE MODE] Player damage buff set to {player.damage_buff}%")
            
            # Also store the multiplier for reference
            player.damage_multiplier = self.rules["player_damage_multiplier"]
    
    def update(self, game_state, dt):
        """Update the game mode state."""
        current_time = pygame.time.get_ticks()
        
        # Get player from game state
        player = game_state.get('player')
        if not player:
            return
        
        # Spawn elite enemies at regular intervals
        if current_time - self.rules["elite_spawn_timer"] > self.rules["elite_spawn_interval"]:
            self._spawn_elites(game_state)
            self.rules["elite_spawn_timer"] = current_time
        
        # Recover player stats over time
        if current_time - self.rules["stat_recovery_timer"] > self.rules["stat_recovery_interval"]:
            self._recover_player_stats(player)
            self.rules["stat_recovery_timer"] = current_time
            print(f"Recovering stats - HP: {player.health}/{player.maximum_health}")
            print(f"Recovering stats - ENERGY: {player.energy}/{player.maximum_energy}")
            print(f"Recovering stats - EXP: {player.exp}/{player.maximum_exp}")
    
    def check_win_condition(self, game_state):
        """No win condition - endless mode."""
        return False
    
    def check_lose_condition(self, game_state):
        """Check if player is dead."""
        player = game_state.get('player')
        return player is None or not player.alive()
    
    def handle_events(self, game_state, event):
        """Handle game events specific to this game mode."""
        pass  # No special event handling needed for this mode
    
    def _spawn_elites(self, game_state):
        """Spawn elite enemies."""
        player = game_state.get('player')
        if not player:
            print("[ERROR] No player found in game state")
            return
            
        # Initialize sprite groups if they don't exist in the game state
        if 'elites' not in game_state:
            game_state['elites'] = pygame.sprite.Group()
        if 'all_sprites' not in game_state:
            game_state['all_sprites'] = pygame.sprite.Group()
            
        elites = game_state['elites']
        all_sprites = game_state['all_sprites']
        
        # Spawn multiple elites
        for i in range(self.rules["elite_spawn_count"]):
            try:
                # Randomly select elite type based on weights
                elite_type = random.choices(
                    self.rules["elite_types"], 
                    weights=self.rules["elite_weights"],
                    k=1
                )[0]
                
                # Create the elite enemy
                if elite_type == "elite1":
                    from Game.entities.enemy_elite1 import Elite_1
                    elite = Elite_1(player)
                elif elite_type == "elite2":
                    from Game.entities.enemy_elite2 import Elite_2
                    elite = Elite_2(player)
                elif elite_type == "elite3":
                    from Game.entities.enemy_elite3 import Elite_3
                    elite = Elite_3(player)
                elif elite_type == "elite4":
                    from Game.entities.enemy_elite4 import Elite_4
                    elite = Elite_4(player)
                
                # Apply elite buffs and damage multiplier
                if hasattr(elite, 'hp'):
                    elite.hp = int(elite.hp * 1.5)  # Make elites tankier
                
                # Apply damage multiplier based on elite type
                if hasattr(elite, 'bullet_damage'):
                    # For ranged elites (Elite_1, Elite_4)
                    if not hasattr(elite, 'original_damage'):
                        elite.original_damage = elite.bullet_damage
                    elite.bullet_damage = int(elite.original_damage * self.rules["enemy_elite_damage_multiplier"])
                    print(f"[ELITE] Spawned {elite_type} with {elite.hp} HP and {elite.bullet_damage} bullet damage (x{self.rules['enemy_elite_damage_multiplier']} multiplier)")
                elif hasattr(elite, 'collide_damage'):
                    # For melee elites (Elite_2, Elite_3)
                    if not hasattr(elite, 'original_damage'):
                        elite.original_damage = elite.collide_damage
                    elite.collide_damage = int(elite.original_damage * self.rules["enemy_elite_damage_multiplier"])
                    print(f"[ELITE] Spawned {elite_type} with {elite.hp} HP and {elite.collide_damage} melee damage (x{self.rules['enemy_elite_damage_multiplier']} multiplier)")
                
                # Add to game
                elites.add(elite)
                all_sprites.add(elite)
                print(f"[ELITE] Spawned {elite_type} at ({elite.rect.x}, {elite.rect.y})")
                
            except Exception as e:
                print(f"[ERROR] Failed to spawn elite: {str(e)}")
                import traceback
                traceback.print_exc()
                
        # Ensure player buffs are properly updated in the UI
        player.update_health_ratio()
        player.health = min(player.health, player.maximum_health)  # Ensure health doesn't exceed max)
    
    def _recover_player_stats(self, player):
        """Gradually recover player stats over time, accounting for buffs."""
        if not player:
            print("[DEBUG] No player object provided for stat recovery")
            return
            
        # Get healing efficiency (default to 0 if not set)
        healing_eff = getattr(player, 'healing_efficiency', 0)
        # Calculate healing bonus (e.g., 10% healing_efficiency = 10% more healing)
        healing_bonus = 1 + (healing_eff / 100.0)  # Convert percentage to multiplier
        
        # Get EXP efficiency (default to 0 if not set)
        exp_eff = getattr(player, 'exp_efficiency', 0)
        # Calculate EXP bonus (e.g., 10% exp_efficiency = 10% more EXP)
        exp_bonus = 1 + (exp_eff / 100.0)  # Convert percentage to multiplier
                   
        # Update health ratio and ensure health doesn't exceed max
        if hasattr(player, 'update_health_ratio') and callable(player.update_health_ratio):
            player.update_health_ratio()
        
        # Recover health (up to max) with healing efficiency bonus
        if hasattr(player, 'health') and hasattr(player, 'maximum_health'):
            if player.health < player.maximum_health:
                base_recovery = player.maximum_health * 0.1  # 10% of max health
                recovery_amount = max(1, int(base_recovery * healing_bonus))
                player.health = min(player.maximum_health, player.health + recovery_amount)
                # Also update current_health to match
                if hasattr(player, 'current_health'):
                    player.current_health = player.health
                print(f"[RECOVERY] Healed {recovery_amount} HP (Healing Eff: +{healing_eff}%)")
        
        # Recover energy (up to max)
        if hasattr(player, 'energy') and hasattr(player, 'maximum_energy'):
            if player.energy < player.maximum_energy:
                recovery_amount = max(0.25, int(player.maximum_energy * 0.1))  # 10% of max energy
                player.energy = min(player.maximum_energy, player.energy + recovery_amount)
                # Also update current_energy to match
                if hasattr(player, 'current_energy'):
                    player.current_energy = player.energy
        
        # Add experience with EXP efficiency bonus
        try:
            # Base EXP gain (1% of max EXP)
            base_exp_gain = max(1, int(getattr(player, 'maximum_exp', 100) * 0.1))
            # Apply EXP efficiency bonus
            exp_gain = int(base_exp_gain * exp_bonus)
            
            # First try using gain_exp method if available
            if hasattr(player, 'gain_exp') and callable(player.gain_exp):
                player.gain_exp(exp_gain)
                print(f"[RECOVERY] Gained {exp_gain} EXP (EXP Eff: +{exp_eff}%)")
            # Fall back to direct exp modification
            elif hasattr(player, 'exp') and hasattr(player, 'maximum_exp'):
                player.exp = min(player.maximum_exp, player.exp + exp_gain)
                # Also update current_exp to match
                if hasattr(player, 'current_exp'):
                    player.current_exp = player.exp
                print(f"[RECOVERY] Gained {exp_gain} EXP (EXP Eff: +{exp_eff}%)")
                
                # Check for level up
                if player.exp >= player.maximum_exp and not player.is_leveling_up:
                    if hasattr(player, 'prepare_level_up') and callable(player.prepare_level_up):
                        player.is_leveling_up = True  # Set level up state
                        player.prepare_level_up()
                    elif hasattr(player, 'level_up') and callable(player.level_up):
                        player.level_up()
        except Exception as e:
            print(f"[ERROR] Error during exp/level up: {str(e)}")
