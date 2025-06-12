import random
import pygame
import math
from . import BaseGameMode, register_game_mode
from ..define import ADD_BOSS, ADD_ENEMY, ADD_ELITE, INCREASE_STAT, SCREEN_WIDTH, SCREEN_HEIGHT

@register_game_mode
class DoubleBozosMode(BaseGameMode):
    """DOUBLE BOZOS game mode - Start with double bosses and get random item drops."""
    
    def __init__(self):
        super().__init__(
            name="DOUBLE BOZOS",
            description="Encounter double bosses at start and items will randomly drop around boss every second; NO LONGER SPAWN NORMAL AND ELITE ENEMIES."
        )
        self.rules = {
            "initial_boss_count": 2,  # Number of bosses to spawn at start
            "item_drop_interval": 1000,  # 1 seconds
            "item_drop_timer": 0,
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
            "boss_defeat_interval": 5000,  # 5 seconds to next wave
            "boss_defeat_timer": 0
        }
        self.is_endless = True  # No win condition, play until defeat
        self.bosses_spawned = False
        self.current_wave = 0
        self.bosses_remaining = 0
        self.sprite_skills_added = 0
    
    def setup(self, game_state):
        """Initialize the DOUBLE BOZOS game mode."""
        # Disable normal enemy and elite spawns
        pygame.time.set_timer(ADD_ENEMY, 0)
        pygame.time.set_timer(ADD_ELITE, 0)
        
        # Set up item drop timer
        self.rules["item_drop_timer"] = pygame.time.get_ticks()
        
        # Apply player buffs
        player = game_state.get('player')
        if player:
            # Increase player max health
            player.maximum_health = int(player.maximum_health * self.rules["player_health_multiplier"])
            player.health = player.maximum_health
            player.update_health_ratio()
            print(f"[DOUBLE BOZOS] Player max health increased to {player.maximum_health}")
        
        # Spawn initial bosses
        self._spawn_initial_bosses(game_state)
    
    def update(self, game_state, dt):
        """Update the game mode state."""
        current_time = pygame.time.get_ticks()
        
        # Spawn item drops at regular intervals
        if current_time - self.rules["item_drop_timer"] > self.rules["item_drop_interval"]:
            self._spawn_random_item(game_state)
            self.rules["item_drop_timer"] = current_time
            
        # Check if all bosses are defeated
        if self.bosses_remaining > 0:
            bosses = game_state.get('bosses', pygame.sprite.Group())
            if len(bosses) == 0:
                if current_time - self.rules["boss_defeat_timer"] > self.rules["boss_defeat_interval"]:
                    self.rules["boss_defeat_timer"] = current_time
                    # All bosses defeated, start next wave
                    self.current_wave += 1
                    self._start_next_wave(game_state)
            else:
                self.rules["boss_defeat_timer"] = current_time
    
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
    
    def _start_next_wave(self, game_state):
        """Start the next wave of bosses with increased difficulty."""
        print(f"[DOUBLE BOZOS] Starting wave {self.current_wave + 1}")
        
        # Calculate stat increases (capped at 50% increase)
        stat_increase = min(0.1 * self.current_wave, 0.5)
        
        # Update boss stats
        self.rules["boss_damage_multiplier"] = 1.0 + stat_increase
        self.rules["boss_speed_multiplier"] = 1.0 + stat_increase
        self.rules["boss_dash_speed_multiplier"] = 1.0 + stat_increase
        
        # Add new sprite skills if not at max
        if self.sprite_skills_added < self.rules["max_sprite_skills"]:
            skills_to_add = min(
                self.rules["sprite_skills_per_wave"],
                self.rules["max_sprite_skills"] - self.sprite_skills_added
            )
            self.sprite_skills_added += skills_to_add
            print(f"[DOUBLE BOZOS] Added {skills_to_add} new sprite skills (Total: {self.sprite_skills_added})")
        
        # Spawn bosses for this wave
        self._spawn_bosses(game_state, self.rules["initial_boss_count"])
    
    def _spawn_initial_bosses(self, game_state):
        """Spawn the initial bosses."""
        if self.bosses_spawned:
            return
            
        player = game_state.get('player')
        if not player:
            print("[ERROR] No player found for boss spawn")
            return
            
        # Get the sprite groups from game state
        bosses = game_state.get('bosses', pygame.sprite.Group())
        all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
        
        # Update game_state with the groups if they weren't there
        game_state['bosses'] = bosses
        game_state['all_sprites'] = all_sprites
        game_state['boss_spawned'] = True
        
        # Start first wave
        self.current_wave = 0
        self._start_next_wave(game_state)
    
    def _spawn_bosses(self, game_state, count):
        """Spawn a specified number of bosses with current wave stats."""
        player = game_state.get('player')
        bosses = game_state.get('bosses', pygame.sprite.Group())
        all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
        
        for i in range(count):
            try:
                from Game.entities.enemy_boss import SkellyBoss
                
                # Calculate spawn position around player with unique angle for each boss
                angle = (2 * math.pi * i) / count  # Evenly distribute bosses in a circle
                angle += random.uniform(-0.2, 0.2)  # Add some randomness to the angle
                
                # Spawn bosses at a good distance from player (400-600 pixels)
                distance = random.uniform(400, 600)
                spawn_x = player.rect.centerx + distance * math.cos(angle)
                spawn_y = player.rect.centery + distance * math.sin(angle)
                
                # Ensure position is within screen bounds with some padding
                spawn_x = max(200, min(int(spawn_x), SCREEN_WIDTH - 200))
                spawn_y = max(200, min(int(spawn_y), SCREEN_HEIGHT - 200))
                
                # Create the boss
                boss = SkellyBoss(player)
                boss.rect.centerx = spawn_x
                boss.rect.centery = spawn_y
                
                # Apply wave-based stat increases
                if hasattr(boss, 'collide_damage'):
                    boss.collide_damage = int(boss.collide_damage * self.rules["boss_damage_multiplier"])
                if hasattr(boss, 'speed'):
                    boss.speed = boss.speed * self.rules["boss_speed_multiplier"]
                if hasattr(boss, 'dash_speed'):
                    boss.dash_speed = boss.dash_speed * self.rules["boss_dash_speed_multiplier"]
                
                # Apply additional sprite skills if any
                if hasattr(boss, 'sprite_skills') and self.sprite_skills_added > 0:
                    boss.sprite_skills = min(
                        len(boss.sprite_skills) + self.sprite_skills_added,
                        len(boss.sprite_skills) * 2  # Don't exceed double the original skills
                    )
                
                # Ensure boss has required health attributes
                if not hasattr(boss, 'max_health'):
                    boss.max_health = 1000  # Default value if not set
                if not hasattr(boss, 'health'):
                    boss.health = boss.max_health
                    
                # Scale health with wave number (optional, can be adjusted)
                boss.max_health = int(boss.max_health * (1 + 0.1 * min(self.current_wave, 5)))
                boss.health = boss.max_health
                
                # Add to game
                bosses.add(boss)
                all_sprites.add(boss)
                self.bosses_remaining += 1
                print(f"[DOUBLE BOZOS] Spawned boss at ({boss.rect.x}, {boss.rect.y}) with {boss.health}/{boss.max_health} HP")
                print(f"[DOUBLE BOZOS] Boss stats - Collide Damage: {boss.collide_damage if hasattr(boss, 'collide_damage') else 'N/A'}, Speed: {boss.speed if hasattr(boss, 'speed') else 'N/A':.2f}")
                if hasattr(boss, 'dash_speed'):
                    print(f"[DOUBLE BOZOS] Boss dash speed: {boss.dash_speed:.2f}")
                if hasattr(boss, 'sprite_skills'):
                    print(f"[DOUBLE BOZOS] Boss sprite skills: {len(boss.sprite_skills)}")
                
            except Exception as e:
                print(f"[ERROR] Failed to spawn boss: {str(e)}")
                import traceback
                traceback.print_exc()
        
        if not self.bosses_spawned:
            self.bosses_spawned = True
        
        print(f"[DOUBLE BOZOS] Wave {self.current_wave + 1} started with {self.bosses_remaining} bosses")
    
    def _spawn_random_item(self, game_state):
        """Spawn a random item in a circle around a random boss."""
        # Get the bosses group
        bosses = game_state.get('bosses', pygame.sprite.Group())
        
        if not bosses:
            print("[DOUBLE BOZOS] No bosses found to spawn items around")
            return
            
        # Get the sprite groups from game state
        exp_items = game_state.get('exp_items', pygame.sprite.Group())
        energy_items = game_state.get('energy_items', pygame.sprite.Group())
        hp_items = game_state.get('hp_items', pygame.sprite.Group())
        all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
        
        # Update game_state with the groups if they weren't there
        game_state['exp_items'] = exp_items
        game_state['energy_items'] = energy_items
        game_state['hp_items'] = hp_items
        game_state['all_sprites'] = all_sprites
        
        # List of possible items to drop with weights for randomness
        item_weights = {
            'HpItem': 0.2,      # 20% chance
            'EnergyItem': 0.2,   # 20% chance
            'ExpItem': 0.6       # 60% chance
        }
        
        try:
            # Choose a random boss to spawn items around
            boss_list = [b for b in bosses if hasattr(b, 'rect') and hasattr(b.rect, 'centerx') and hasattr(b.rect, 'centery')]
            if not boss_list:
                print("[DOUBLE BOZOS] No valid boss found for item spawn")
                return
                
            boss = random.choice(boss_list)
            boss_x = boss.rect.centerx
            boss_y = boss.rect.centery
            
            print(f"[DOUBLE BOZOS] Selected boss at ({boss_x}, {boss_y})")
            
            # Choose random item type based on weights
            item_type = random.choices(
                list(item_weights.keys()),
                weights=list(item_weights.values()),
                k=1
            )[0]
            
            print(f"[DOUBLE BOZOS] Spawning {self.rules['item_drop_count']} {item_type}s around boss at ({boss_x}, {boss_y})")
            
            # Import item classes with correct paths
            for _ in range(self.rules["item_drop_count"]):
                try:
                    # Calculate spawn position in a circle around the boss for EACH item
                    # Random distance from boss (300-400 pixels)
                    distance = random.uniform(300, 400)
                    # Random angle in a full circle
                    angle = random.uniform(0, 2 * math.pi)
                    
                    # Calculate spawn position relative to boss
                    spawn_x = int(boss_x + distance * math.cos(angle))
                    spawn_y = int(boss_y + distance * math.sin(angle))
                    
                    print(f"[DEBUG] Spawning {item_type} at ({spawn_x}, {spawn_y})")

                    from Game.entities.items import HpItem, EnergyItem, ExpItem
                    
                    # Create a simple container just to satisfy the item constructor
                    class DummyContainer:
                        def __init__(self, x, y):
                            self.x = x
                            self.y = y
                            self.size = 30  # Default size for items
                        
                        def get_position_x(self):
                            return self.x
                        
                        def get_position_y(self):
                            return self.y
                        
                        def get_size(self):
                            return self.size
                    
                    # Create the item with a dummy container
                    item = None
                    if item_type == 'HpItem':
                        item = HpItem(DummyContainer(0, 0))
                    elif item_type == 'EnergyItem':
                        item = EnergyItem(DummyContainer(0, 0))
                    elif item_type == 'ExpItem':
                        item = ExpItem(DummyContainer(0, 0))
                    
                    if item and hasattr(item, 'rect'):
                        # Set the position directly
                        item.rect.center = (spawn_x, spawn_y)
                        
                        # Debug output
                        print(f"[DEBUG] Created {item_type} at ({spawn_x}, {spawn_y})")
                        print(f"[DEBUG] Item rect: {item.rect} at position ({item.rect.x}, {item.rect.y})")
                        print(f"[DEBUG] Item center: {item.rect.center}")
                        
                        # Create a new update method that does nothing to position
                        original_update = item.update if hasattr(item, 'update') else None
                        def new_update():
                            if original_update:
                                original_update()
                        item.update = new_update
                        
                        # Add to the appropriate item group based on type
                        if isinstance(item, HpItem):
                            hp_items.add(item)
                            game_state['hp_items'] = hp_items
                        elif isinstance(item, EnergyItem):
                            energy_items.add(item)
                            game_state['energy_items'] = energy_items
                        elif isinstance(item, ExpItem):
                            exp_items.add(item)
                            game_state['exp_items'] = exp_items
                        
                        # Add to all_sprites if not already there
                        if hasattr(item, 'rect') and item not in all_sprites:
                            all_sprites.add(item)
                            game_state['all_sprites'] = all_sprites
                        
                        print(f"[DOUBLE BOZOS] Spawned {item_type} at ({spawn_x}, {spawn_y})")
                        
                except ImportError as e:
                    print(f"[ERROR] Failed to import item classes: {e}")
                    import traceback
                    traceback.print_exc()
                
        except Exception as e:
            print(f"[ERROR] Failed to spawn item: {str(e)}")
            import traceback
            traceback.print_exc()
