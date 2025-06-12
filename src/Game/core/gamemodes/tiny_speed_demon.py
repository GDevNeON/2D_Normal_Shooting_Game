"""
TINY SPEED DEMON Game Mode

This module implements the TINY SPEED DEMON game mode where everything is faster and smaller.
"""
import pygame
import random
import os
import sys
from . import BaseGameMode, register_game_mode
from ..define import ADD_ENEMY, ADD_ELITE, ADD_BOSS, SCREEN_WIDTH, SCREEN_HEIGHT

# Import player sprites
try:
    # Try relative import first for both male and female sprites
    from ...entities.player_female import (
        female_idle_sprite, 
        female_run_sprite, 
        female_idle_sprite_left, 
        female_run_sprite_left
    )
    from ...entities.player_male import (
        male_idle_sprite,
        male_run_sprite,
        male_idle_sprite_left,
        male_run_sprite_left
    )
    print("[TINY SPEED DEMON] Successfully imported player sprites")
except ImportError as e:
    print(f"[WARNING] Could not import player sprites: {e}")
    # Fallback in case the direct import fails
    female_idle_sprite = female_run_sprite = female_idle_sprite_left = female_run_sprite_left = []
    male_idle_sprite = male_run_sprite = male_idle_sprite_left = male_run_sprite_left = []
    print("[WARNING] Could not import player sprites. Player resizing may not work correctly.")

@register_game_mode
class TinySpeedDemonMode(BaseGameMode):
    """TINY SPEED DEMON game mode - Everything is faster and smaller!"""
    
    def __init__(self):
        super().__init__(
            name="tiny_speed_demon",  # Must match the ID in config.py
            description="Player and enemies are smaller and faster; bullets move faster; BOSS included!"
        )
        self.rules = {
            "player_speed_multiplier": 2.0,
            "player_size_multiplier": 0.5,
            "enemy_speed_multiplier": 1.8,
            "enemy_size_multiplier": 0.5,
            "boss_size_multiplier": 0.6,  # Boss will be 60% of original size
            "boss_speed_multiplier": 2,
            "bullet_speed_multiplier": 1.5,
            "enemy_spawn_interval": 3000,  # 3 seconds
            "enemy_spawn_timer": 0,
            "elite_spawn_interval": 10000,  # 10 seconds
            "elite_spawn_timer": 0,
            "boss_spawn_interval": 300000,  # 5 minutes
            "boss_spawn_timer": 0,
            "disable_boss": False
        }
        self.is_endless = True  # No win condition, play until defeat
        self.boss_spawned = False

    def setup(self, game_state):
        """Initialize the TINY SPEED DEMON game mode."""
        # Disable boss spawns
        pygame.time.set_timer(ADD_BOSS, 0)
        
        # Set up timers
        current_time = pygame.time.get_ticks()
        self.rules["enemy_spawn_timer"] = current_time
        self.rules["elite_spawn_timer"] = current_time
        
        # Modify player stats
        player = game_state.get('player')
        if not player:
            return
            
        print("[TINY SPEED DEMON] Setting up player with size multiplier:", self.rules["player_size_multiplier"])
        
        # Store original speed if not already stored
        if not hasattr(player, '_original_speed'):
            player._original_speed = player.speed
        
        # Apply speed multiplier to original speed to avoid compounding
        player.speed = player._original_speed * self.rules["player_speed_multiplier"]
        
        # Get the sprite lists from the player's module
        try:
            # Import the player modules
            from ...entities.player_female import (
                female_idle_sprite, female_run_sprite,
                female_idle_sprite_left, female_run_sprite_left
            )
            from ...entities.player_male import (
                male_idle_sprite, male_run_sprite,
                male_idle_sprite_left, male_run_sprite_left
            )
            
            size_multiplier = self.rules["player_size_multiplier"]
            print(f"[TINY SPEED DEMON] Scaling player sprites by {size_multiplier}x")
            
            # Scale player sprites based on size_multiplier
            def scale_sprite_list(original_list, multiplier):
                scaled = []
                for frame in original_list:
                    if frame:  # Only scale if frame exists
                        new_size = (
                            max(1, int(frame.get_width() * multiplier)),
                            max(1, int(frame.get_height() * multiplier))
                        )
                        scaled.append(pygame.transform.smoothscale(frame, new_size))
                return scaled
            
            # Check player type by checking the class
            from ...entities.player_male import Player_Male
            is_male = isinstance(player, Player_Male)
            
            # Load original sprites if not already stored
            if not hasattr(self, '_original_male_idle'):
                self._original_male_idle = male_idle_sprite.copy()
                self._original_male_run = male_run_sprite.copy()
                self._original_male_idle_left = male_idle_sprite_left.copy()
                self._original_male_run_left = male_run_sprite_left.copy()
                self._original_female_idle = female_idle_sprite.copy()
                self._original_female_run = female_run_sprite.copy()
                self._original_female_idle_left = female_idle_sprite_left.copy()
                self._original_female_run_left = female_run_sprite_left.copy()
            
            if is_male:
                # Scale from original sprites
                player._scaled_idle = scale_sprite_list(self._original_male_idle, size_multiplier)
                player._scaled_run = scale_sprite_list(self._original_male_run, size_multiplier)
                player._scaled_idle_left = scale_sprite_list(self._original_male_idle_left, size_multiplier)
                player._scaled_run_left = scale_sprite_list(self._original_male_run_left, size_multiplier)
                
                # Update global sprite lists for male
                male_idle_sprite[:] = player._scaled_idle
                male_run_sprite[:] = player._scaled_run
                male_idle_sprite_left[:] = player._scaled_idle_left
                male_run_sprite_left[:] = player._scaled_run_left
            else:
                # Scale from original sprites
                player._scaled_idle = scale_sprite_list(self._original_female_idle, size_multiplier)
                player._scaled_run = scale_sprite_list(self._original_female_run, size_multiplier)
                player._scaled_idle_left = scale_sprite_list(self._original_female_idle_left, size_multiplier)
                player._scaled_run_left = scale_sprite_list(self._original_female_run_left, size_multiplier)
                
                # Update global sprite lists for female
                female_idle_sprite[:] = player._scaled_idle
                female_run_sprite[:] = player._scaled_run
                female_idle_sprite_left[:] = player._scaled_idle_left
                female_run_sprite_left[:] = player._scaled_run_left
            
            print(f"[TINY SPEED DEMON] Player sprites scaled. New sizes: {player._scaled_idle[0].get_size() if player._scaled_idle else 'N/A'}")
            
            # Replace the player's animation methods with our patched versions
            def patched_idle_anim(player_instance, clock):
                try:
                    # Update the animation frame index
                    player_instance.idle_time += clock.get_time()
                    if player_instance.idle_time >= 200:
                        player_instance.idle_time = 0
                        player_instance.idle_index = (player_instance.idle_index + 1) % len(player_instance._scaled_idle)
                    
                    # Set the appropriate sprite based on direction
                    if player_instance.direction == "right":
                        player_instance.surf = player_instance._scaled_idle[player_instance.idle_index % len(player_instance._scaled_idle)]
                    else:
                        player_instance.surf = player_instance._scaled_idle_left[player_instance.idle_index % len(player_instance._scaled_idle_left)]
                    
                    # Update rect size to match new surface
                    old_center = player_instance.rect.center
                    player_instance.rect = player_instance.surf.get_rect(center=old_center)
                except Exception as e:
                    print(f"Error in patched_idle_anim: {e}")
            
            def patched_run_anim(player_instance, clock):
                try:
                    # Update the animation frame index
                    player_instance.run_time += clock.get_time()
                    if player_instance.run_time >= 125:
                        player_instance.run_time = 0
                        player_instance.run_index = (player_instance.run_index + 1) % len(player_instance._scaled_run)
                    
                    # Set the appropriate sprite based on direction
                    if player_instance.direction == "right":
                        player_instance.surf = player_instance._scaled_run[player_instance.run_index % len(player_instance._scaled_run)]
                    else:
                        player_instance.surf = player_instance._scaled_run_left[player_instance.run_index % len(player_instance._scaled_run_left)]
                    
                    # Update rect size to match new surface
                    old_center = player_instance.rect.center
                    player_instance.rect = player_instance.surf.get_rect(center=old_center)
                except Exception as e:
                    print(f"Error in patched_run_anim: {e}")
            
            # Replace the animation methods with our patched versions
            # Create bound methods using lambda to properly bind the player instance
            player.idle_anim = lambda clock: patched_idle_anim(player, clock)
            player.run_anim = lambda clock: patched_run_anim(player, clock)
            
            # Reset animation indices and update the current surface
            player.idle_index = 0
            player.run_index = 0
            player.idle_time = 0
            player.run_time = 0
            
            # Update the current surface and rect
            old_center = player.rect.center
            if hasattr(player, '_scaled_idle') and player._scaled_idle:
                player.surf = player._scaled_idle[player.idle_index % len(player._scaled_idle)]
                player.rect = player.surf.get_rect(center=old_center)
            
            # Scale the hitbox to match the new size
            if hasattr(player, 'hitbox'):
                player.hitbox.width = player.rect.width * 0.7
                player.hitbox.height = player.rect.height * 0.7
                player.hitbox.center = player.rect.center
            
            print(f"[TINY SPEED DEMON] Player resized: {player.rect.size}")
            
        except Exception as e:
            print(f"[TINY SPEED DEMON] Error resizing player: {e}")
        
        print(f"[TINY SPEED DEMON] Player speed: {player.speed}, size: {player.rect.size if hasattr(player, 'rect') else 'N/A'}")

    def update(self, game_state, dt):
        """Update the game mode state."""
        current_time = pygame.time.get_ticks()
        
        # Spawn normal enemies at regular intervals
        if current_time - self.rules["enemy_spawn_timer"] > self.rules["enemy_spawn_interval"]:
            self._spawn_enemy(game_state)
            self.rules["enemy_spawn_timer"] = current_time
        
        # Spawn elite enemies at regular intervals
        if current_time - self.rules["elite_spawn_timer"] > self.rules["elite_spawn_interval"]:
            self._spawn_elite(game_state)
            self.rules["elite_spawn_timer"] = current_time
        
        # Spawn boss after interval if not already spawned
        if not self.boss_spawned and current_time - self.rules["boss_spawn_timer"] > self.rules["boss_spawn_interval"]:
            self._spawn_boss(game_state)
            self.boss_spawned = True
        
        # Update all enemies and boss to be faster and smaller
        self._update_enemies(game_state)
        
        # Update bullets to be faster
        self._update_bullets(game_state)

    def _spawn_enemy(self, game_state):
        """Spawn a new enemy with modified stats."""
        player = game_state.get('player')
        enemies = game_state.get('enemies', pygame.sprite.Group())
        all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
        
        if not player or not hasattr(player, 'get_position_x') or not hasattr(player, 'get_position_y'):
            print("[TINY SPEED DEMON] Player reference is invalid")
            return
            
        # Create enemy with modified stats - use Normal enemy class which initializes sprites properly
        from Game.entities.enemy import Normal
        enemy = Normal(player)
        
        # Apply speed modification
        enemy.speed *= self.rules["enemy_speed_multiplier"]
        
        # Store original sprite for reference if not already stored
        if not hasattr(enemy, '_original_sprite'):
            enemy._original_sprite = enemy.sprite.copy() if hasattr(enemy, 'sprite') and enemy.sprite else None
        
        # Resize enemy sprite and hitbox
        if hasattr(enemy, 'sprite') and enemy.sprite:
            # Create a new list to store scaled sprites
            scaled_sprites = []
            
            # Scale each frame of the sprite animation
            for frame in enemy.sprite:
                # Get original size if available, otherwise use current size
                original_size = frame.get_size()
                new_size = (
                    int(original_size[0] * self.rules["enemy_size_multiplier"]),
                    int(original_size[1] * self.rules["enemy_size_multiplier"])
                )
                # Scale the sprite frame
                scaled_frame = pygame.transform.scale(frame, new_size)
                scaled_sprites.append(scaled_frame)
            
            # Update the enemy's sprite list with scaled versions
            enemy.sprite = scaled_sprites
            
            # Update the current surface and rect
            if enemy.sprite:
                enemy.surf = enemy.sprite[0].copy()
                enemy.rect = enemy.surf.get_rect(center=enemy.rect.center)
                
                # Also update the original sprite for reference
                if hasattr(enemy, '_original_sprite'):
                    enemy._original_sprite = enemy.sprite.copy()
        
        # Also update the hitbox separately to ensure it matches the sprite size
        if hasattr(enemy, 'surf') and enemy.surf:
            old_center = enemy.rect.center
            enemy.rect.size = enemy.surf.get_size()
            enemy.rect.center = old_center
        
        # Generate a random position around the player using the enemy's built-in method
        enemy.generate_random_position(player)
        
        # Add to groups
        enemies.add(enemy)
        all_sprites.add(enemy)
        
        print(f"[TINY SPEED DEMON] Spawned enemy at {enemy.rect.center}")

    def _spawn_elite(self, game_state):
        """Spawn an elite enemy with modified stats."""
        from Game.entities.enemy_elite1 import Elite_1
        
        player = game_state.get('player')
        elites = game_state.get('elites', pygame.sprite.Group())
        all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
        
        if not player or not hasattr(player, 'get_position_x') or not hasattr(player, 'get_position_y'):
            print("[TINY SPEED DEMON] Player reference is invalid")
            return
            
        # Randomly select elite type
        elite_type = random.choice(["Elite_1", "Elite_2", "Elite_3", "Elite_4"])  # Add all your elite types here
        
        # Create the selected elite enemy
        if elite_type == "Elite_1":
            from Game.entities.enemy_elite1 import Elite_1
            elite = Elite_1(player)
        elif elite_type == "Elite_2":
            from Game.entities.enemy_elite2 import Elite_2
            elite = Elite_2(player)
        elif elite_type == "Elite_3":
            from Game.entities.enemy_elite3 import Elite_3
            elite = Elite_3(player)
        elif elite_type == "Elite_4":
            from Game.entities.enemy_elite4 import Elite_4
            elite = Elite_4(player)
        else:
            # Fallback to Elite_1 if type is not recognized
            from Game.entities.enemy_elite1 import Elite_1
            elite = Elite_1(player)
        
        # Apply speed modification (elites are faster)
        elite.speed *= self.rules["enemy_speed_multiplier"] * 1.2
        
        # Store original sprite for reference if not already stored
        if not hasattr(elite, '_original_sprite'):
            elite._original_sprite = elite.sprite.copy() if hasattr(elite, 'sprite') and elite.sprite else None
        
        # Resize elite sprite and hitbox
        if hasattr(elite, 'sprite') and elite.sprite:
            # Create a new list to store scaled sprites
            scaled_sprites = []
            size_multiplier = self.rules["enemy_size_multiplier"] * 0.9  # Slightly bigger than normal enemies
            
            # Scale each frame of the sprite animation
            for frame in elite.sprite:
                # Get original size if available, otherwise use current size
                original_size = frame.get_size()
                new_size = (
                    int(original_size[0] * size_multiplier),
                    int(original_size[1] * size_multiplier)
                )
                # Scale the sprite frame
                scaled_frame = pygame.transform.scale(frame, new_size)
                scaled_sprites.append(scaled_frame)
            
            # Update the elite's sprite list with scaled versions
            elite.sprite = scaled_sprites
            
            # Scale the dash sprite if it exists
            if hasattr(elite, 'dash_sprite'):
                if elite.dash_sprite:
                    # If dash_sprite is a list of frames
                    if isinstance(elite.dash_sprite, list):
                        scaled_dash_sprites = []
                        for frame in elite.dash_sprite:
                            new_size = (
                                int(frame.get_width() * size_multiplier),
                                int(frame.get_height() * size_multiplier)
                            )
                            scaled_dash_sprites.append(pygame.transform.scale(frame, new_size))
                        elite.dash_sprite = scaled_dash_sprites
                    # If dash_sprite is a single surface
                    else:
                        new_size = (
                            int(elite.dash_sprite.get_width() * size_multiplier),
                            int(elite.dash_sprite.get_height() * size_multiplier)
                        )
                        elite.dash_sprite = pygame.transform.scale(elite.dash_sprite, new_size)
            
            # Update the current surface and rect
            if elite.sprite:
                elite.surf = elite.sprite[0].copy()
                elite.rect = elite.surf.get_rect(center=elite.rect.center)
                
                # Also update the original sprite for reference
                if hasattr(elite, '_original_sprite'):
                    elite._original_sprite = elite.sprite.copy()
        
        # Also update the hitbox separately to ensure it matches the sprite size
        if hasattr(elite, 'surf') and elite.surf:
            old_center = elite.rect.center
            elite.rect.size = elite.surf.get_size()
            elite.rect.center = old_center
        
        # Generate a random position around the player using the enemy's built-in method
        elite.generate_random_position(player)
        
        # Add to groups
        elites.add(elite)
        all_sprites.add(elite)
        
        print(f"[TINY SPEED DEMON] Spawned elite at {elite.rect.center}")

    def _spawn_boss(self, game_state):
        """Spawn a boss with modified stats for Tiny Speed Demon mode."""
        try:
            from Game.entities.enemy_boss import SkellyBoss
            
            player = game_state.get('player')
            bosses = game_state.get('bosses', pygame.sprite.Group())
            all_sprites = game_state.get('all_sprites', pygame.sprite.Group())
            
            if not player:
                print("[TINY SPEED DEMON] No player found for boss spawn")
                return
                
            # Choose a random position around the edge of the screen
            side = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left
            if side == 0:  # top
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = -100
            elif side == 1:  # right
                x = SCREEN_WIDTH + 100
                y = random.randint(100, SCREEN_HEIGHT - 100)
            elif side == 2:  # bottom
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = SCREEN_HEIGHT + 100
            else:  # left
                x = -100
                y = random.randint(100, SCREEN_HEIGHT - 100)
            
            # Create the boss with the player reference
            boss = SkellyBoss(player)
            # Set the position manually after creation
            boss.rect.center = (x, y)
            
            # Store original values for reference
            boss._original_speed = boss.speed
            if hasattr(boss, 'dash_speed'):
                boss._original_dash_speed = boss.dash_speed
            
            # Scale boss sprites if they exist
            if hasattr(boss, 'sprite') and boss.sprite:
                # Store original sprite for reference
                if not hasattr(boss, '_original_sprite'):
                    boss._original_sprite = boss.sprite.copy()
                
                # Create a new list to store scaled sprites
                scaled_sprites = []
                size_multiplier = self.rules["boss_size_multiplier"]
                
                # Scale each frame of the sprite animation
                for frame in boss.sprite:
                    if frame:
                        original_size = frame.get_size()
                        new_size = (
                            int(original_size[0] * size_multiplier),
                            int(original_size[1] * size_multiplier)
                        )
                        # Scale the sprite frame
                        scaled_frame = pygame.transform.smoothscale(frame, new_size)
                        scaled_sprites.append(scaled_frame)
                
                # Update the boss's sprite list with scaled versions
                boss.sprite = scaled_sprites
                
                # Update the current surface and rect
                if boss.sprite:
                    boss.surf = boss.sprite[0].copy()
                    boss.rect = boss.surf.get_rect(center=boss.rect.center)
                    
                    # Update hitbox to match scaled size
                    if hasattr(boss, 'hitbox_radius'):
                        boss.hitbox_radius = int(boss.hitbox_radius * size_multiplier)
            
            # Add to sprite groups
            bosses.add(boss)
            all_sprites.add(boss)
            
            # Update game state
            game_state['bosses'] = bosses
            game_state['all_sprites'] = all_sprites
            game_state['boss_spawned'] = True
            
            print(f"[TINY SPEED DEMON] Boss spawned at ({x}, {y})")
            
        except Exception as e:
            print(f"[TINY SPEED DEMON] Error spawning boss: {e}")
            import traceback
            traceback.print_exc()

    def _update_enemies(self, game_state):
        """Update all enemies and boss to be faster and smaller."""
        enemies = game_state.get('enemies', pygame.sprite.Group())
        elites = game_state.get('elites', pygame.sprite.Group())
        bosses = game_state.get('bosses', pygame.sprite.Group())
        
        # Process normal enemies
        for enemy in enemies:
            # Apply speed modification if not already done
            if not hasattr(enemy, '_speed_modified'):
                if hasattr(enemy, '_original_speed'):
                    enemy.speed = enemy._original_speed * self.rules["enemy_speed_multiplier"]
                else:
                    enemy._original_speed = enemy.speed
                    enemy.speed *= self.rules["enemy_speed_multiplier"]
                enemy._speed_modified = True
            
            # Apply size modification if not already done
            if not hasattr(enemy, '_size_modified'):
                size_multiplier = self.rules["enemy_size_multiplier"]
                
                # Store original sprite for reference if not already stored
                if hasattr(enemy, 'sprite') and enemy.sprite and not hasattr(enemy, '_original_sprite'):
                    enemy._original_sprite = enemy.sprite.copy()
                
                # Scale sprites if they exist
                if hasattr(enemy, 'sprite') and enemy.sprite:
                    # Create a new list to store scaled sprites
                    scaled_sprites = []
                    
                    # Scale each frame of the sprite animation
                    for frame in enemy.sprite:
                        if frame:
                            original_size = frame.get_size()
                            new_size = (
                                int(original_size[0] * size_multiplier),
                                int(original_size[1] * size_multiplier)
                            )
                            # Scale the sprite frame
                            scaled_frame = pygame.transform.smoothscale(frame, new_size)
                            scaled_sprites.append(scaled_frame)
                    
                    # Update the enemy's sprite list with scaled versions
                    enemy.sprite = scaled_sprites
                    
                    # Update the current surface and rect
                    if enemy.sprite:
                        enemy.surf = enemy.sprite[0].copy()
                        old_center = enemy.rect.center
                        enemy.rect = enemy.surf.get_rect()
                        enemy.rect.center = old_center
                else:
                    # Fallback to just scaling the rectangle if no sprite list is available
                    old_center = enemy.rect.center
                    enemy.rect.width = int(enemy.rect.width * size_multiplier)
                    enemy.rect.height = int(enemy.rect.height * size_multiplier)
                    enemy.rect.center = old_center
                
                # Update hitbox if it exists
                if hasattr(enemy, 'hitbox_radius'):
                    enemy.hitbox_radius = int(enemy.hitbox_radius * size_multiplier)
                
                enemy._size_modified = True
        
        # Process elite enemies
        for elite in elites:
            # Apply speed modification if not already done
            if not hasattr(elite, '_speed_modified'):
                if hasattr(elite, '_original_speed'):
                    elite.speed = elite._original_speed * self.rules["enemy_speed_multiplier"]
                else:
                    elite._original_speed = elite.speed
                    elite.speed *= self.rules["enemy_speed_multiplier"] * 1.2
                elite._speed_modified = True
            
            # Apply size modification if not already done
            if not hasattr(elite, '_size_modified') and hasattr(elite, 'sprite') and elite.sprite:
                # Store original sprites if not already stored
                if not hasattr(elite, '_original_sprite'):
                    elite._original_sprite = elite.sprite.copy()
                
                # Slightly bigger than normal enemies (90% of normal size)
                size_multiplier = self.rules["enemy_size_multiplier"] * 0.9
                
                # Scale each frame of the sprite animation
                scaled_sprites = []
                for frame in elite._original_sprite:
                    if frame:
                        new_size = (
                            int(frame.get_width() * size_multiplier),
                            int(frame.get_height() * size_multiplier)
                        )
                        scaled_sprites.append(pygame.transform.scale(frame, new_size))
                
                # Update the sprite list
                elite.sprite = scaled_sprites
                
                # Update current surface and rect
                if elite.sprite:
                    elite.surf = elite.sprite[0].copy()
                    elite.rect = elite.surf.get_rect(center=elite.rect.center)
                
                elite._size_modified = True

    def _update_bullets(self, game_state):
        """Update all bullets to be faster."""
        bullets = game_state.get('bullets', pygame.sprite.Group())
        
        for bullet in bullets:
            if not hasattr(bullet, '_speed_modified'):
                bullet.speed *= self.rules["bullet_speed_multiplier"]
                bullet._speed_modified = True

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
