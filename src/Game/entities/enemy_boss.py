import pygame
import math
import random
import time

from ..core.define import *
from ..entities.enemy import Enemy
from ..entities.items import Items
from ..managers.image_manager import *
from ..managers.sound_manager import SoundManager

class SwordSkill(pygame.sprite.Sprite):
    """Sword skill animation for the boss first phase skill"""
    def __init__(self, x, y, player):
        super(SwordSkill, self).__init__()
        self.sprite = []
        self.animation_speed = 500  # Time between frames in ms
        self.player = player
        self.damage = 15
        self.damage_dealt = False
        
        # Load sprites
        for path in swordskill_path:
            try:
                img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                # Scale using BOSS_SIZE
                img = pygame.transform.scale_by(img, BOSS_SIZE * 1.5)  # Slightly smaller than boss size
                self.sprite.append(img)
            except Exception as e:
                print(f"Error loading sword skill sprite {path}: {e}")
                # Create a placeholder surface if loading fails
                size = int(100 * BOSS_SIZE * 1.5)
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(surf, (255, 0, 255), (0, 0, size, size))
                self.sprite.append(surf)
        
        if not self.sprite:  # If no sprites were loaded
            size = int(100 * BOSS_SIZE * 1.5)
            self.sprite = [pygame.Surface((size, size), pygame.SRCALPHA)]
            pygame.draw.rect(self.sprite[0], (255, 0, 255), (0, 0, size, size))
        
        self.surf = self.sprite[0]
        self.rect = self.surf.get_rect(center=(x, y))
        self.sprite_index = 0
        self.sprite_time = 0

    def update(self, clock):
        # Update animation
        self.sprite_time += clock.get_time()
        if self.sprite_time >= self.animation_speed:
            self.sprite_index += 1
            if self.sprite_index >= len(self.sprite):
                # Remove sprite if animation is complete
                self.kill()
                return
            
            self.surf = self.sprite[self.sprite_index]
            self.sprite_time = 0
            
            # Check for collision with player on the 4th frame
            if self.sprite_index == 3 and not self.damage_dealt:
                if self.rect.colliderect(self.player.rect):
                    self.player.take_damage(self.damage)
                    self.damage_dealt = True


class SwordCast(pygame.sprite.Sprite):
    """Sword cast animation for the boss second phase skill"""
    def __init__(self, x, y, player):
        super(SwordCast, self).__init__()
        self.sprite = []
        self.animation_speed = 500  # Time between frames in ms
        self.player = player
        self.damage = 25
        self.damage_dealt = False
        
        # Load sprites
        for path in swordcast_path:
            try:
                img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                # Scale using BOSS_SIZE
                img = pygame.transform.scale_by(img, BOSS_SIZE * 1.5)  # Slightly smaller than boss size
                self.sprite.append(img)
            except Exception as e:
                print(f"Error loading sword cast sprite {path}: {e}")
                # Create a placeholder surface if loading fails
                size = int(120 * BOSS_SIZE * 1.5)
                surf = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(surf, (255, 165, 0), (0, 0, size, size))
                self.sprite.append(surf)
        
        if not self.sprite:  # If no sprites were loaded
            size = int(120 * BOSS_SIZE * 1.5)
            self.sprite = [pygame.Surface((size, size), pygame.SRCALPHA)]
            pygame.draw.rect(self.sprite[0], (255, 165, 0), (0, 0, size, size))
        
        self.surf = self.sprite[0]
        self.rect = self.surf.get_rect(center=(x, y))
        self.sprite_index = 0
        self.sprite_time = 0

    def update(self, clock):
        # Update animation
        self.sprite_time += clock.get_time()
        if self.sprite_time >= self.animation_speed:
            self.sprite_index += 1
            if self.sprite_index >= len(self.sprite):
                # Remove sprite if animation is complete
                self.kill()
                return
            
            self.surf = self.sprite[self.sprite_index]
            self.sprite_time = 0
            
            # Check for collision with player on the 3rd frame
            if self.sprite_index == 3 and not self.damage_dealt:
                if self.rect.colliderect(self.player.rect):
                    self.player.take_damage(self.damage)
                    self.damage_dealt = True


class SkellyFeather(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(SkellyFeather, self).__init__()
        from ..managers.image_manager import skelly_feather_sprite, load_feather_sprite
        
        # Ensure the feather sprite is loaded
        load_feather_sprite()
        
        # Use the pre-loaded feather sprite
        if skelly_feather_sprite is not None:
            self.image = skelly_feather_sprite
            print(f"[Feather {id(self)}] Created at position: ({int(x)}, {int(y)})")
        else:
            # Create a placeholder if loading fails
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 200, 0), (20, 20), 20)  # Yellow circle
            print(f"[Feather {id(self)}] Created placeholder sprite")
        
        self.rect = self.image.get_rect(center=(x, y))
        self.collected = False
        
        # Animation properties
        self.float_speed = 0.5
        self.float_range = 2
        self.original_y = y
        self.time_offset = random.uniform(0, 10)  # Randomize float pattern
        self.rotation_angle = 0
        self.rotation_speed = random.uniform(-2, 2)  # Random rotation speed
        self.last_update = pygame.time.get_ticks()
        
        # Store the original image for rotation
        self.original_image = self.image.copy()

    def update(self):
        """Update feather animation"""
        # Float up and down
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_update) / 1000.0  # Convert to seconds
        self.last_update = current_time
        
        # Calculate floating effect
        self.rect.y = self.original_y + math.sin((current_time / 1000) * self.float_speed + self.time_offset) * self.float_range
        
        # Rotate the feather
        self.rotation_angle += self.rotation_speed * dt * 60  # Scale by dt and a factor for speed
        self.rotation_angle %= 360  # Keep angle within 0-360 degrees
        
        # Rotate the image
        if hasattr(self, 'original_image'):
            self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
            
            # Update the rect to keep the center position
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)


class SkellyBoss(Enemy):
    """Skelly boss with two phases"""
    def __init__(self, player, game_mode="normal"):
        super(SkellyBoss, self).__init__(player)
        # Basic attributes
        self.name = "Skelly"
        # Use BOSS_SIZE for scaling, with a base size of 80
        self.base_size = 80
        self.size = int(self.base_size * BOSS_SIZE)
        self.spawn_radius = 800  # Spawn further away than regular enemies
        self.phase = 1
        self.game_mode = game_mode
        
        # Store screen dimensions for feather spawning
        self.screen_width = 1920  # Default values, will be updated in update
        self.screen_height = 1080
        
        # Stats for phase 1
        self.health = 10000
        self.max_health = 10000
        self.speed = 2
        self.dash_speed = 6  # Slower dash speed (was 10)
        self.collide_damage = 25
        
        # Trail effect for dash
        self.trail_positions = []
        self.max_trail_length = 10  # Number of trail images to show
        
        # Animation attributes
        # Load sprites
        self.sprite = []
        # Use the pre-loaded sprites from image_manager
        if skelly_walk_sprite:  # Check if sprites are loaded in image_manager
            self.sprite = [sprite.copy() for sprite in skelly_walk_sprite]
            # Scale each sprite to the correct size
            self.sprite = [pygame.transform.scale(sprite, (self.size, self.size)) for sprite in self.sprite]
            print(f"[Boss] Loaded and scaled {len(self.sprite)} walk sprites from image_manager to {self.size}x{self.size}")
        else:
            # Fallback to loading directly if not in image_manager
            for path in skelly_walk_path:
                try:
                    img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                    # Scale the sprite to the target size
                    img = pygame.transform.scale(img, (self.size, self.size))
                    self.sprite.append(img)
                except Exception as e:
                    print(f"Error loading boss sprite {path}: {e}")
                    # Create a placeholder surface if loading fails
                    surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    pygame.draw.rect(surf, (255, 0, 0), (0, 0, self.size, self.size))
                    self.sprite.append(surf)
        
        if not self.sprite:  # If no sprites were loaded
            # Create a placeholder surface with the correct size
            self.sprite = [pygame.Surface((self.size, self.size), pygame.SRCALPHA)]
            pygame.draw.rect(self.sprite[0], (255, 0, 0), (0, 0, self.size, self.size))
            
        self.surf = self.sprite[0]
        self.rect = self.surf.get_rect()
        self.sprite_index = 0
        self.sprite_time = 0
        self.direction = "right"  # Default direction
        self.generate_random_position(player)
        
        # Attack timers
        self.dash_cooldown = 5000  # 5 seconds
        self.last_dash_time = 0
        self.skill_cooldown = 10000  # 10 seconds
        self.last_skill_time = 0
        self.is_using_skill = False
        self.skill_duration = 10000  # 10 seconds skill duration
        self.skill_start_time = 0
        self.sword_spawn_timer = 0
        
        # Phase transition
        self.is_transitioning = False
        self.transition_start_time = 0
        self.transition_duration = 5000  # 5 seconds
        
        # Load phase transition sprites
        self.phase_transition_sprite = []
        # Use the pre-loaded sprites from image_manager
        if skelly_transform_sprite:  # Check if sprites are loaded in image_manager
            self.phase_transition_sprite = [sprite.copy() for sprite in skelly_transform_sprite]
            # Scale each sprite to the correct size
            self.phase_transition_sprite = [pygame.transform.scale(sprite, (self.size, self.size)) 
                                          for sprite in self.phase_transition_sprite]
            print(f"[Boss] Loaded and scaled {len(self.phase_transition_sprite)} transition sprites to {self.size}x{self.size}")
        else:
            # Fallback to loading directly if not in image_manager
            for path in skele_phasetrans_path:
                try:
                    img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                    # Scale the sprite to the target size
                    img = pygame.transform.scale(img, (self.size, self.size))
                    self.phase_transition_sprite.append(img)
                except Exception as e:
                    print(f"Error loading phase transition sprite {path}: {e}")
                    # Create a placeholder surface if loading fails
                    surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    pygame.draw.rect(surf, (255, 165, 0), (0, 0, 100 * BOSS_SIZE, 100 * BOSS_SIZE))
                    self.phase_transition_sprite.append(surf)
        
        if not self.phase_transition_sprite:  # If no sprites were loaded
            # Create a placeholder surface with BOSS_SIZE scaling
            placeholder_size = int(100 * BOSS_SIZE)
            self.phase_transition_sprite = [pygame.Surface((placeholder_size, placeholder_size), pygame.SRCALPHA)]
            pygame.draw.rect(self.phase_transition_sprite[0], (255, 165, 0), (0, 0, placeholder_size, placeholder_size))
        
        self.phase_transition_index = 0
        self.phase_transition_time = 0
        
        # Final phase attributes
        self.feathers = []
        self.total_feathers = 10
        self.feathers_collected = 0
        self.feather_timer = 0
        self.defeated = False
        self.defeat_time = 0
        self.feather_collection_time = 30000  # 30 seconds to collect feathers
        
        # Respawn timer (for endless mode)
        self.respawn_time = 300000  # 5 minutes in milliseconds
        self.death_time = 0
        
    def update(self, player, bullet_group, all_sprites, clock, skill_sprites=None):
        """Update boss state and behavior"""
        current_time = pygame.time.get_ticks()
        
        # Update screen dimensions from the display surface
        if hasattr(player, 'screen'):
            self.screen_width = player.screen.get_width()
            self.screen_height = player.screen.get_height()
        
        # Handle defeated state
        if self.defeated:
            if self.phase == 2:
                # Boss is immediately defeated in phase 2
                print("Boss defeated in phase 2")
                self.death_time = current_time
                pygame.event.post(pygame.event.Event(BOSS_DEFEATED))
                self.kill()
                return True
            return
            
        # Render trail effect if dashing
        if hasattr(self, 'trail_positions') and self.trail_positions:
            # Draw each trail position on the screen
            for trail in self.trail_positions:
                # Create a rect for the trail image
                trail_rect = self.dash_sprite.get_rect(center=(trail['x'], trail['y']))
                # Draw the trail on the screen
                SCREEN.blit(trail['surf'], trail_rect)
                
            # Remove old trail positions (older than 400ms)
            self.trail_positions = [t for t in self.trail_positions if current_time - t['time'] < 400]
        
        # Check for bullet collisions
        for bullet in bullet_group:
            if pygame.sprite.collide_rect(self, bullet):
                self.take_damage(bullet.damage)
                bullet.kill()
                
        # Handle phase 2 defeat
        if self.phase == 2 and self.health <= 0 and not self.defeated:
            print("Boss entering feather collection phase")
            self.defeated = True
            self.defeat_time = current_time
            
            # Spawn feathers around the arena
            for i in range(self.total_feathers):
                angle = (i / self.total_feathers) * 2 * math.pi
                radius = 800  # Radius from boss center
                x = self.rect.centerx + radius * math.cos(angle)
                y = self.rect.centery + radius * math.sin(angle)
                
                # Create feather and add to sprite groups
                feather = SkellyFeather(x, y)
                self.feathers.append(feather)
                all_sprites.add(feather)
            
            # Set health to 0 to show defeat state
            self.health = 0
            return
        # Check for phase transition
        if self.is_transitioning:
            self.update_phase_transition(clock)
            return
            
        # Check for dash attack
        if hasattr(self, 'is_dashing') and self.is_dashing:
            dash_complete = self.perform_dash_attack(player, clock)
            if dash_complete:
                self.is_dashing = False
                self.last_dash_time = current_time
                self.surf = self.orig_sprite  # Restore original sprite
                # Clear trail positions after dash completes
                self.trail_positions = []
            return
        
        # Check for skill use
        if self.is_using_skill:
            self.update_skill(player, all_sprites, clock, skill_sprites)
            return
            
        # Try a dash attack if cooldown is over
        if current_time - self.last_dash_time >= self.dash_cooldown:
            if random.random() < 0.01:  # 1% chance per frame to dash
                self.start_dash(player)
                return
        
        # Try a skill if cooldown is over
        if current_time - self.last_skill_time >= self.skill_cooldown:
            if random.random() < 0.005:  # 0.5% chance per frame to use skill
                if self.phase == 1:
                    skill = self.use_sword_skill(player)
                else:
                    skill = self.use_sword_cast(player)
                if skill and skill_sprites is not None:
                    skill_sprites.add(skill)
                    all_sprites.add(skill)
                return
        
        # Basic movement when not dashing or using skills
        self.move_towards_player(player)
        self.load_sprite(clock)
        
    def start_dash(self, player):
        """Start the dash attack
        
        Args:
            player: The player object to target with the dash
        """
        if not self.is_using_skill and not self.is_transitioning:
            self.perform_dash_attack(player, pygame.time.Clock())
            
    def use_sword_skill(self, player):
        """Use the sword skill (phase 1)
        
        Args:
            player: The player object to target with the skill
        """
        if not self.is_using_skill and not self.is_transitioning and self.phase == 1:
            self.start_skill(pygame.time.get_ticks())
            return SwordSkill(self.rect.centerx, self.rect.centery, player)
        return None
        
    def use_sword_cast(self, player):
        """Use the sword cast (phase 2)
        
        Args:
            player: The player object to target with the cast
        """
        if not self.is_using_skill and not self.is_transitioning and self.phase == 2:
            self.start_skill(pygame.time.get_ticks())
            return SwordCast(self.rect.centerx, self.rect.centery, player)
        return None
        
    def transition_to_phase2(self):
        """Transition to phase 2"""
        if self.phase == 1 and not self.is_transitioning:
            print("Starting phase 2 transition...")
            self.phase = 2
            self.health = self.max_health  # Restore full health for phase 2
            self.speed *= 1.5  # Increase speed in phase 2
            self.damage = 30  # Increase damage in phase 2
            
            # Store the current position for later
            old_center = self.rect.center
            
            # Use the pre-loaded sprites from image_manager
            from ..managers.image_manager import skellyphase2_walk_sprite
            
            self.sprite = []
            if skellyphase2_walk_sprite:  # If we have loaded sprites
                print("Using pre-loaded phase 2 sprites")
                for sprite in skellyphase2_walk_sprite:
                    try:
                        # Make a copy and scale it to the boss size
                        img = pygame.transform.scale(sprite.copy(), (self.size, self.size))
                        self.sprite.append(img)
                    except Exception as e:
                        print(f"Error processing phase 2 boss sprite: {e}")
                        # Create a placeholder surface if processing fails
                        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                        pygame.draw.rect(surf, (255, 128, 0), (0, 0, self.size, self.size))
                        self.sprite.append(surf)
            else:
                # Fallback to loading from paths if pre-loaded sprites aren't available
                print("No pre-loaded phase 2 sprites, falling back to path loading")
                from ..managers.image_manager import skellyphase2_walk_path
                for path in skellyphase2_walk_path:
                    try:
                        print(f"Loading phase 2 sprite: {path}")
                        img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                        img = pygame.transform.scale(img, (self.size, self.size))
                        self.sprite.append(img)
                    except Exception as e:
                        print(f"Error loading phase 2 boss sprite {path}: {e}")
                        # Create a placeholder surface if loading fails
                        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                        pygame.draw.rect(surf, (255, 128, 0), (0, 0, self.size, self.size))
                        self.sprite.append(surf)
            
            if not self.sprite:  # If no sprites were loaded
                print("No phase 2 sprites loaded, creating placeholder")
                self.sprite = [pygame.Surface((self.size, self.size), pygame.SRCALPHA)]
                pygame.draw.rect(self.sprite[0], (255, 128, 0), (0, 0, self.size, self.size))
            
            # Ensure we have a valid surface
            if not isinstance(self.sprite[0], pygame.Surface):
                print("First sprite is not a surface, creating fallback")
                self.sprite[0] = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.rect(self.sprite[0], (255, 0, 255), (0, 0, self.size, self.size))
            
            self.surf = self.sprite[0]
            self.rect = self.surf.get_rect()
            self.rect.center = old_center  # Restore position
            self.sprite_index = 0
            self.sprite_time = 0
            self.last_skill_time = pygame.time.get_ticks()  # Reset skill cooldown
            print("Phase 2 transition complete")
    
    def load_sprite(self, clock):
        """Update boss animation"""
        if not hasattr(self, 'sprite') or not self.sprite:
            # Initialize sprites if they don't exist
            self.sprite = [pygame.Surface((self.size, self.size), pygame.SRCALPHA)]
            color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
            pygame.draw.rect(self.sprite[0], color, (0, 0, self.size, self.size))
            self.surf = self.sprite[0]
            self.rect = self.surf.get_rect(center=getattr(self, 'rect', (0, 0)).center)
            return
            
        self.left_or_right()
        self.sprite_time += clock.get_time()
        
        if self.sprite_index >= len(self.sprite):
            self.sprite_index = 0
        
        if self.sprite_time >= 250:  # Update sprite every 250ms
            try:
                # Ensure we have a valid sprite at the current index
                if not (0 <= self.sprite_index < len(self.sprite)):
                    self.sprite_index = 0
                    
                current_sprite = self.sprite[self.sprite_index]
                
                # If it's a string, try to load it as an image path
                if isinstance(current_sprite, str):
                    try:
                        img_path = (mod_path / current_sprite).resolve()
                        current_sprite = pygame.image.load(str(img_path)).convert_alpha()
                        current_sprite = pygame.transform.scale(current_sprite, (self.size, self.size))
                        self.sprite[self.sprite_index] = current_sprite  # Cache the loaded surface
                    except Exception as e:
                        print(f"Error loading sprite {current_sprite}: {e}")
                        # Create a placeholder if loading fails
                        current_sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                        color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
                        pygame.draw.rect(current_sprite, color, (0, 0, self.size, self.size))
                        self.sprite[self.sprite_index] = current_sprite
                
                # Ensure we have a valid surface
                if not isinstance(current_sprite, pygame.Surface):
                    current_sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                    color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
                    pygame.draw.rect(current_sprite, color, (0, 0, self.size, self.size))
                
                # Flip sprite based on direction
                if hasattr(self, 'direction') and self.direction == "left":
                    current_sprite = pygame.transform.flip(current_sprite, True, False)
                
                # Update the surface and maintain position
                old_center = getattr(self.rect, 'center', (0, 0))
                self.surf = current_sprite
                self.rect = self.surf.get_rect(center=old_center)
                
                # Move to next sprite
                self.sprite_index = (self.sprite_index + 1) % len(self.sprite)
                self.sprite_time = 0
                
            except Exception as e:
                print(f"Critical error in load_sprite: {e}")
                # Fallback to a colored rectangle if something goes wrong
                self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.rect(self.surf, (255, 0, 0), (0, 0, self.size, self.size))
    
    def start_dash(self, player):
        """Start the dash attack
        
        Args:
            player: The player object to target with the dash
        """
        # Save player position at the start of dash
        self.dash_target_x = player.get_position_x()
        self.dash_target_y = player.get_position_y()
        self.is_dashing = True
        self.dash_start_time = pygame.time.get_ticks()
        self.dash_duration = 800  # 800ms dash duration (was 500ms)
        self.dash_distance = 0
        
        # Clear trail positions
        self.trail_positions = []
        
        # Calculate dash vector
        dx = self.dash_target_x - self.rect.centerx
        dy = self.dash_target_y - self.rect.centery
        self.dash_distance = math.sqrt(dx**2 + dy**2)
        
        # Save original position
        self.dash_start_x = self.rect.centerx
        self.dash_start_y = self.rect.centery
        
        # Normalize direction
        if self.dash_distance > 0:
            self.dash_dx = dx / self.dash_distance
            self.dash_dy = dy / self.dash_distance
        else:
            self.dash_dx = 0
            self.dash_dy = 0
            
        # Create attack surface
        try:
            # Try to use preloaded sprites from image manager if available
            from ..managers.image_manager import skelly_atk_sprite, skellyphase2_atk_sprite
            
            if self.phase == 1 and skelly_atk_sprite is not None:
                # Use phase 1 attack sprite
                attack_sprite = skelly_atk_sprite.copy()
            elif self.phase == 2 and skellyphase2_atk_sprite is not None:
                # Use phase 2 attack sprite
                attack_sprite = skellyphase2_atk_sprite.copy()
            else:
                # Fallback to loading directly
                if self.phase == 1:
                    attack_sprite = pygame.image.load((mod_path / skelly_atk).resolve()).convert_alpha()
                else:
                    attack_sprite = pygame.image.load((mod_path / skellyphase2_atk).resolve()).convert_alpha()
            
            # Scale the sprite to match boss size
            attack_sprite = pygame.transform.scale(attack_sprite, (self.size, self.size))
            
            # Flip based on direction
            if self.direction == "left":
                attack_sprite = pygame.transform.flip(attack_sprite, True, False)
                
            # Save the old center position
            old_center = self.rect.center
            
            # Set the attack sprite
            self.dash_sprite = attack_sprite
            self.orig_sprite = self.surf  # Save the original sprite
            self.surf = attack_sprite
            
            # Maintain position
            self.rect = self.surf.get_rect(center=old_center)
            
        except Exception as e:
            print(f"Error loading attack sprite: {e}")
            # Create a placeholder if loading fails
            attack_sprite = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
            pygame.draw.rect(attack_sprite, color, (0, 0, self.size, self.size))
            self.dash_sprite = attack_sprite
            self.surf = attack_sprite
            
    def perform_dash_attack(self, player, clock):
        """Perform a dash attack toward the player"""
        # This is now handled in the update method with animation
        current_time = pygame.time.get_ticks()
        dash_progress = min(1.0, (current_time - self.dash_start_time) / self.dash_duration)
        
        if dash_progress < 1.0:
            # Smoothly interpolate position
            new_x = self.dash_start_x + (self.dash_dx * self.dash_distance * dash_progress)
            new_y = self.dash_start_y + (self.dash_dy * self.dash_distance * dash_progress)
            
            # Store current position for trail effect (every few frames)
            if random.random() < 0.3:  # 30% chance to add a trail position each frame
                # Create a copy of the dash sprite with reduced opacity for trail effect
                trail_surf = self.dash_sprite.copy()
                trail_surf.set_alpha(120)  # 47% opacity
                
                # Add current position and sprite to trail
                self.trail_positions.append({
                    'x': self.rect.centerx,
                    'y': self.rect.centery,
                    'surf': trail_surf,
                    'time': current_time
                })
                
                # Limit trail length
                if len(self.trail_positions) > self.max_trail_length:
                    self.trail_positions.pop(0)
            
            # Update position
            self.rect.centerx = new_x
            self.rect.centery = new_y
            
            # Keep attack sprite
            self.surf = self.dash_sprite
            return False  # Dash not complete
        else:
            # Dash complete
            self.is_dashing = False
            self.last_dash_time = current_time
            
            # Restore original sprite
            if hasattr(self, 'orig_sprite'):
                self.surf = self.orig_sprite
            return True  # Dash complete
                
    def start_skill(self, current_time):
        """Start using a skill"""
        self.is_using_skill = True
        self.skill_start_time = current_time
        self.sword_spawn_timer = 0
    
    def update_skill(self, player, all_sprites, clock, skill_sprites):
        """Update skill animation and effects"""
        current_time = pygame.time.get_ticks()
        
        # Try to use preloaded sprites from image manager if available
        try:
            from ..managers.image_manager import skelly_skill_sprite, skelly_transform_sprite
            
            # Set the appropriate skill animation
            if self.phase == 1:
                skill_sprites_to_use = skelly_skill_sprite
                spawn_interval = 500  # Spawn swords every 0.5 seconds
                spawn_count = 5  # Spawn 5 swords at once
                skill_radius = 1000
                skill_class = SwordSkill
                # Fallback to paths if needed
                fallback_paths = skelly_1st_skill_path
            else:
                skill_sprites_to_use = []
                # Check if we have 2nd phase skill sprites
                from ..managers.image_manager import skelly_2nd_skill1, skelly_2nd_skill2
                try:
                    # Create sprite array if it doesn't exist
                    phase2_sprites = []
                    for path in [skelly_2nd_skill1, skelly_2nd_skill2]:
                        img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                        img = pygame.transform.scale(img, (self.size, self.size))
                        phase2_sprites.append(img)
                    skill_sprites_to_use = phase2_sprites
                except Exception as e:
                    print(f"Error loading phase 2 skill sprites: {e}")
                    # Use phase 1 sprites as fallback
                    if skelly_skill_sprite:
                        skill_sprites_to_use = skelly_skill_sprite
                
                spawn_interval = 1000  # Spawn swords every 1 second
                spawn_count = 10  # Spawn 10 swords at once
                skill_radius = 1500
                skill_class = SwordCast
                # Fallback to paths if needed
                fallback_paths = skelly_2nd_skill_path
            
            # Update skill animation
            self.sprite_time += clock.get_time()
            if self.sprite_time >= 250:
                # If we have preloaded sprites, use them
                if skill_sprites_to_use and len(skill_sprites_to_use) > 0:
                    frame_index = (current_time // 250) % len(skill_sprites_to_use)
                    try:
                        # Make a copy of the sprite and scale it to the boss's size
                        current_sprite = pygame.transform.scale(
                            skill_sprites_to_use[frame_index], 
                            (self.size, self.size)
                        )
                        
                        # Flip sprite based on direction
                        if hasattr(self, 'direction') and self.direction == "left":
                            current_sprite = pygame.transform.flip(current_sprite, True, False)
                            
                        # Save the old center position
                        old_center = self.rect.center
                        
                        # Update the surface
                        self.surf = current_sprite
                        
                        # Maintain position
                        self.rect = self.surf.get_rect(center=old_center)
                    except Exception as e:
                        print(f"Error using skill sprite: {e}")
                        # Create a placeholder surface if processing fails
                        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                        color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
                        pygame.draw.rect(self.surf, color, (0, 0, self.size, self.size))
                # Fall back to paths if no preloaded sprites
                else:
                    try:
                        frame_index = (current_time // 250) % len(fallback_paths)
                        path = fallback_paths[frame_index]
                        
                        # Load the sprite if it's a path
                        if isinstance(path, str):
                            img = pygame.image.load((mod_path / path).resolve()).convert_alpha()
                            img = pygame.transform.scale(img, (self.size, self.size))
                            
                            # Flip if needed
                            if hasattr(self, 'direction') and self.direction == "left":
                                img = pygame.transform.flip(img, True, False)
                            
                            # Save position
                            old_center = self.rect.center
                            
                            # Update surface
                            self.surf = img
                            
                            # Maintain position
                            self.rect = self.surf.get_rect(center=old_center)
                    except Exception as e:
                        print(f"Error loading skill sprite from path: {e}")
                        # Create a placeholder surface if loading fails
                        self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                        color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
                        pygame.draw.rect(self.surf, color, (0, 0, self.size, self.size))
                
                self.sprite_time = 0
        except Exception as e:
            print(f"Critical error in update_skill: {e}")
            # Create a placeholder surface if something goes terribly wrong
            self.surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            color = (255, 0, 0) if self.phase == 1 else (0, 0, 255)
            pygame.draw.rect(self.surf, color, (0, 0, self.size, self.size))
        
        # Spawn skill effects
        self.sword_spawn_timer += clock.get_time()
        if self.sword_spawn_timer >= spawn_interval:
            for _ in range(spawn_count):
                # Generate random position around boss
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(200, skill_radius)
                x = self.rect.centerx + radius * math.cos(angle)
                y = self.rect.centery + radius * math.sin(angle)
                
                # Create sword skill
                sword = skill_class(x, y, player)
                skill_sprites.add(sword)
                all_sprites.add(sword)
            
            self.sword_spawn_timer = 0
        
        # End skill after duration
        if current_time - self.skill_start_time >= self.skill_duration:
            self.is_using_skill = False
            
            # Reset to normal walking animation
            if self.phase == 1:
                self.sprite = skelly_walk_path.copy()
            else:
                self.sprite = skellyphase2_walk_path.copy()
    
    def start_phase_transition(self):
        """Start the transition to phase 2"""
        self.is_transitioning = True
        self.transition_start_time = pygame.time.get_ticks()
        self.health = 0  # Ensure health stays at 0 during transition
        
    def update_phase_transition(self, clock):
        """Update phase transition animation"""
        current_time = pygame.time.get_ticks()
        
        # Update animation
        self.phase_transition_time += clock.get_time()
        if self.phase_transition_time >= 250:
            frame_index = (current_time // 250) % len(self.phase_transition_sprite)
            self.surf = self.phase_transition_sprite[frame_index]
            self.phase_transition_time = 0
        
        # End transition after duration
        if current_time - self.transition_start_time >= self.transition_duration:
            self.is_transitioning = False
            self.phase = 2
            
            # Upgrade boss for phase 2
            self.health = 1500
            self.max_health = 1500
            self.speed = 3
            self.dash_speed = 15
            self.collide_damage = 40
            
            # Set phase 2 sprites
            self.sprite = skellyphase2_walk_path.copy()
            self.surf = self.sprite[0]
            
    def handle_phase2_defeat(self, player, all_sprites):
        """Handle boss defeat in phase 2"""
        current_time = pygame.time.get_ticks()
        
        # If this is the first frame of defeat, spawn feathers
        if self.defeated and not self.feathers:
            print("\n=== BOSS DEFEATED - SPAWNING FEATHERS ===")
            print(f"Current time: {current_time}")
            
            # Get screen dimensions
            screen_width = getattr(player, 'screen_width', self.screen_width)
            screen_height = getattr(player, 'screen_height', self.screen_height)
            print(f"Screen size: {screen_width}x{screen_height}")
            
            # Calculate spawn positions in a circle around the boss
            center_x, center_y = self.rect.center
            radius = min(screen_width, screen_height) * 0.3  # 30% of screen size
            
            print(f"Boss center: ({center_x}, {center_y}), Spawn radius: {radius}")
            
            for i in range(self.total_feathers):
                try:
                    # Calculate angle for this feather (evenly distributed in a circle)
                    angle = (2 * math.pi * i) / self.total_feathers
                    
                    # Calculate position
                    x = center_x + math.cos(angle) * radius
                    y = center_y + math.sin(angle) * radius
                    
                    # Ensure position is within screen bounds with padding
                    padding = 100
                    x = max(padding, min(x, screen_width - padding))
                    y = max(padding, min(y, screen_height - padding))
                    
                    print(f"Creating feather {i+1} at ({int(x)}, {int(y)}) with angle {math.degrees(angle):.1f}°")
                    
                    # Create feather
                    feather = SkellyFeather(x, y)
                    self.feathers.append(feather)
                    
                    # Add to all_sprites if available
                    if all_sprites is not None:
                        all_sprites.add(feather)
                        print(f"[Boss] Added feather {i+1} to all_sprites")
                    else:
                        print("WARNING: all_sprites group is None!")
                    
                except Exception as e:
                    import traceback
                    print(f"ERROR creating feather {i+1}: {e}")
                    print(traceback.format_exc())
            
            print("\n=== FEATHER SPAWNING COMPLETE ===")
            print(f"Total feathers created: {len(self.feathers)}")
            print(f"all_sprites count: {len(all_sprites) if all_sprites else 0}")
            
            # Set timeout for feather collection
            self.feather_collection_start = current_time
            self.defeat_time = current_time
            
            # Initialize indicator font if needed
            if not hasattr(self, 'font'):
                try:
                    self.font = pygame.font.Font(None, 36)  # Try to load default font
                except:
                    # Fallback to basic font if default fails
                    self.font = pygame.font.SysFont('Arial', 36)
        
        # Check if timeout for feather collection has expired
        if self.defeated and self.feathers and current_time - self.defeat_time >= self.feather_collection_time:
            print("Feather collection time expired - boss regenerating")
            
            # Boss recovers if time expired
            self.defeated = False
            self.health = int(self.max_health * 0.5)  # 50% health regeneration
            
            # Remove any remaining feathers
            for feather in self.feathers:
                if hasattr(feather, 'kill'):
                    feather.kill()
            self.feathers = []
            self.feathers_collected = 0
            
            return False  # Boss resumes normal behavior
        
        return True  # Continue in defeated state while waiting for feathers or timeout
    
    def collect_feather(self, feather):
        """Mark a feather as collected"""
        if feather in self.feathers:
            self.feathers_collected += 1
            self.feathers.remove(feather)
            feather.kill()
            return True
        return False
    
    def take_damage(self, amount):
        """Take damage and check for phase transition"""
        if self.defeated:  # Don't take damage if already in defeated state
            return False
            
        self.health -= amount
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()
        
        # Check for phase 1 to 2 transition
        if self.phase == 1 and self.health <= 0 and not self.is_transitioning:
            self.health = 0
            self.start_phase_transition()  # Start phase transition
            return False  # Not fully defeated yet
            
        # Check for phase 2 defeat
        if self.phase == 2 and self.health <= 0 and not self.defeated:
            self.health = 0
            self.defeated = True
            self.defeat_time = pygame.time.get_ticks()
            return True  # Will be handled in update
            
        return False
