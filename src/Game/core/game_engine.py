import pygame
import random
import sys
import importlib
import pkgutil
from types import ModuleType

sys.path.insert(0, r"./src/Menu")

# Import from our reorganized modules
from ..core.define import *
from ..entities.player_male import Player_Male
from ..entities.player_female import Player_Female
from ..entities.enemy import Normal
from ..entities.enemy_elite1 import Elite_1
from ..entities.enemy_elite2 import Elite_2
from ..entities.enemy_elite3 import Elite_3
from ..entities.enemy_elite4 import Elite_4
from ..entities.enemy_boss import SkellyBoss
from ..entities.items import *
from ..utils.functions import *
from ..managers.image_manager import *
from ..components.background import Background
from ..components.camera import *
from ..managers.sound_manager import SoundManager, grassplain, grassplain_boss

# Import VictoryScene from Menu.scenes
from Menu.scenes.victory_scene import VictoryScene

# Import game modes
from .gamemodes import GAME_MODES

pygame.mixer.init()
pygame.init()

def load_custom_game_mode(mode_name):
    """Dynamically load a custom game mode by name."""
    if not mode_name:
        return None
        
    # Try to import the module if it's not already loaded
    if mode_name not in GAME_MODES:
        try:
            module_name = f"Game.core.gamemodes.{mode_name}"
            importlib.import_module(module_name)
        except ImportError as e:
            print(f"[ERROR] Failed to load game mode {mode_name}: {e}")
            return None
    
    return GAME_MODES.get(mode_name)

def Run_Game(current_mode=0, character_select=0, custom_mode_name=None, scene_manager=None):
    # Debug info about parameters
    print(f"[DEBUG] Run_Game called with: mode={current_mode}, character={character_select}, custom_mode={custom_mode_name}")
    print(f"[DEBUG] scene_manager provided: {scene_manager is not None}")
    
    # Clear all timers when starting a new game
    from ..core.define import clear_all_timers, ADD_BOSS, ADD_ENEMY, ADD_ELITE, INCREASE_STAT
    clear_all_timers()
    
    # Set up default game timers
    pygame.time.set_timer(ADD_ENEMY, 7000)     # Spawn normal enemies every 7 seconds
    pygame.time.set_timer(ADD_ELITE, 40000)    # Spawn elite enemies every 40 seconds
    pygame.time.set_timer(INCREASE_STAT, 60000) # Increase stats every 60 seconds
    pygame.time.set_timer(ADD_BOSS, 300000)     # Spawn boss after 5 minutes
    
    # Initialize game mode
    game_mode = None
    if custom_mode_name and isinstance(custom_mode_name, str):
        game_mode = load_custom_game_mode(custom_mode_name.lower())
    
    clock = pygame.time.Clock()
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    SoundManager.play_music(grassplain, loops=-1)
    
    # Game state groups
    enemies         = pygame.sprite.Group()
    elites          = pygame.sprite.Group()
    bosses          = pygame.sprite.Group()
    boss_skills     = pygame.sprite.Group()
    player_bullets  = pygame.sprite.Group()
    elite_bullets   = pygame.sprite.Group()
    exp_items       = pygame.sprite.Group()
    energy_items    = pygame.sprite.Group()
    hp_items        = pygame.sprite.Group()
    items_group     = pygame.sprite.Group()
    all_sprites     = pygame.sprite.Group()
    
    # Create camera
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
    
    # Create player
    if character_select == 1:
        player = Player_Male()
    else:
        player = Player_Female()
    all_sprites.add(player)
    
    background = Background(background_sprite)
    
    # Game state dictionary to pass to game modes
    game_state = {
        'player': player,
        'enemies': enemies,
        'elites': elites,
        'bosses': bosses,
        'boss_skills': boss_skills,
        'player_bullets': player_bullets,
        'elite_bullets': elite_bullets,
        'exp_items': exp_items,
        'energy_items': energy_items,
        'hp_items': hp_items,
        'items_group': items_group,
        'all_sprites': all_sprites,
        'camera': camera
    }
    
    # Boss related variables
    boss_spawned = False
    boss_death_time = 0
    boss_respawn_time = 300000  # 5 minutes (in milliseconds)
    
    flag = 0
    c_mode = current_mode
    is_paused = False
    game_won = False
    
    difficulty_multiplier = 1.0
    
    # Initialize game mode if custom mode is selected
    if game_mode:
        print(f"[DEBUG] Initializing game mode: {game_mode.name}")
        game_mode.setup(game_state)
        # Update game mode based on custom mode rules
        if game_mode.rules.get('disable_normal_enemies', False):
            pygame.time.set_timer(ADD_ENEMY, 0)  # Disable normal enemies
        if game_mode.rules.get('disable_boss', False):
            pygame.time.set_timer(ADD_BOSS, 0)   # Disable boss
    else:
        # Set up default game mode based on current_mode (normal/endless)
        if current_mode == 1:  # Normal mode
            # Normal mode settings (default timers)
            pygame.time.set_timer(ADD_ENEMY, 7000)
            pygame.time.set_timer(ADD_ELITE, 40000)
            pygame.time.set_timer(INCREASE_STAT, 60000)
            pygame.time.set_timer(ADD_BOSS, 300000)
        else:  # Endless mode
            # Endless mode settings (faster spawns)
            pygame.time.set_timer(ADD_ENEMY, 5000)
            pygame.time.set_timer(ADD_ELITE, 30000)
            pygame.time.set_timer(INCREASE_STAT, 45000)
            pygame.time.set_timer(ADD_BOSS, 300000)
    
    # Gameplay loop
    running = True
    show_help = False  # Track if we're showing the help screen
    last_time = pygame.time.get_ticks()
    
    while running:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time
        
        pressed_keys = pygame.key.get_pressed()
        SCREEN.fill(Black)            

        # Update game mode if active
        if game_mode and not is_paused and not show_help and not player.is_leveling_up:
            game_mode.update(game_state, dt)
            
            # Check win/lose conditions from game mode
            if game_mode.check_lose_condition(game_state):
                print(f"[DEBUG] Game over - {game_mode.name} lose condition met")
                from Menu.scenes.game_over_scene import GameOverScene
                return GameOverScene(SCREEN, player.score)
                
            if game_mode.check_win_condition(game_state):
                print(f"[DEBUG] Game won - {game_mode.name} win condition met")
                return VictoryScene(SCREEN, player.score)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Let game mode handle events first if it wants to
            if game_mode and not is_paused and not show_help and not player.is_leveling_up:
                game_mode.handle_events(game_state, event)
            
            # Handle keyboard events
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if show_help:
                        # If showing help, go back to pause menu
                        show_help = False
                    else:
                        # Otherwise, exit to main menu
                        running = False
                elif event.key == K_p and not show_help:  # Only allow pausing when not in help screen
                    is_paused = not is_paused
                    if is_paused:
                        SoundManager.play_pause_game()
                elif event.key == K_q and player.energy >= player.maximum_energy and player.burst_clock < player.burst_time and not is_paused and not player.is_leveling_up:
                    player.energy = 0
                    player.burst = True
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if is_paused:
                    if show_help:
                        # Handle help screen back button
                        button_rects = player.ui.draw_pause_menu(SCREEN, player, show_help=True)
                        if button_rects.get('back') and button_rects['back'].collidepoint(mouse_pos):
                            SoundManager.play_button_select()
                            show_help = False
                    else:
                        # Handle pause menu button clicks
                        button_rects = player.ui.draw_pause_menu(SCREEN, player)
                        if button_rects.get('resume') and button_rects['resume'].collidepoint(mouse_pos):
                            SoundManager.play_button_select()
                            is_paused = False
                        elif button_rects.get('menu') and button_rects['menu'].collidepoint(mouse_pos):
                            SoundManager.play_button_select()
                            SoundManager.play_button_select()
                            pygame.mouse.set_visible(True)
                            return  # Return to main menu
                        elif button_rects.get('help') and button_rects['help'].collidepoint(mouse_pos):
                            SoundManager.play_button_select()
                            show_help = True
                
                # Handle level up menu
                elif player.is_leveling_up:
                    player.handle_level_up_selection(mouse_pos)
                
                # Handle pause button click
                else:
                    pause_button = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
                    if pause_button.collidepoint(mouse_pos):
                        is_paused = not is_paused
                        if is_paused:
                            SoundManager.play_pause_game()
                            show_help = False  # Reset help screen when pausing
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY and not player.is_leveling_up and not is_paused:  # Không tạo enemy khi đang level up hoặc pause
                for _ in range(20):  # Tạo 20 kẻ địch
                    new_enemy = Normal(player)
                    new_enemy.set_speed(new_enemy.get_speed() * difficulty_multiplier)
                    new_enemy.set_hp(new_enemy.get_hp() * difficulty_multiplier)
                    new_enemy.set_damage(new_enemy.get_damage() * difficulty_multiplier)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                    
            if event.type == INCREASE_STAT and not is_paused:
                difficulty_multiplier += 0.1
                 
            # Các sự kiện của enemy Elite
            if event.type == ADD_ELITE and not player.is_leveling_up and not is_paused:  # Không tạo elite khi đang level up hoặc pause
                rand = random.randint(1, 4)
                if rand == 1:
                    new_elite = Elite_1(player)
                    new_elite.set_bullet_damage(new_elite.get_bullet_damage() * difficulty_multiplier)
                elif rand == 2:
                    new_elite = Elite_2(player)
                elif rand == 3:
                    new_elite = Elite_3(player)
                else:
                    new_elite = Elite_4(player)
                    new_elite.set_bullet_damage(new_elite.get_bullet_damage() * difficulty_multiplier)
                new_elite.set_speed(new_elite.get_speed() * difficulty_multiplier)
                new_elite.set_hp(new_elite.get_hp() * difficulty_multiplier)
                new_elite.set_damage(new_elite.get_damage() * difficulty_multiplier)

                elites.add(new_elite)
                all_sprites.add(new_elite)
                
            # Handle boss events
            if event.type == ADD_BOSS and not is_paused and not player.is_leveling_up and not boss_spawned:
                print(f"[DEBUG] ADD_BOSS event triggered. Mode: {'NORMAL' if c_mode == 0 else 'ENDLESS'}, Game won: {game_won}")
                # Clear the timer after the boss spawns to prevent multiple spawns
                pygame.time.set_timer(ADD_BOSS, 0)
                if (c_mode == 1 and not game_won) or (c_mode == 0 and pygame.time.get_ticks() - boss_death_time >= boss_respawn_time):
                    print("[DEBUG] Attempting to spawn boss...")
                    # Switch to boss music
                    SoundManager.play_music(grassplain_boss, loops=-1)
                    # Create the boss
                    boss = SkellyBoss(player, game_mode="normal" if c_mode == 1 else "endless")
                    bosses.add(boss)
                    all_sprites.add(boss)
                    boss_spawned = True
                    print(f"[DEBUG] Boss spawned at {pygame.time.get_ticks()//1000} seconds")
                    # Set up boss timers
                    pygame.time.set_timer(BOSS_DASH, 5000)  # Dash every 5 seconds
                    pygame.time.set_timer(BOSS_SKILL_1, 10000)  # Skill 1 every 10 seconds
                else:
                    print(f"[DEBUG] Boss spawn conditions not met. Mode: {c_mode}, Game won: {game_won}, Time since death: {pygame.time.get_ticks() - boss_death_time}ms")
                    
            # Handle boss dash event
            if event.type == BOSS_DASH and boss_spawned:
                for boss in bosses:  # Get the boss from the bosses group
                    if not boss.defeated:
                        boss.start_dash(player)  # Pass the player object to the dash attack
                    
            if event.type == BOSS_SKILL_1 and boss_spawned:
                for boss in bosses:  # Get the boss from the bosses group
                    if boss.phase == 1 and not boss.defeated:
                        skill = boss.use_sword_skill(player)  # Pass player to sword skill
                        if skill:
                            boss_skills.add(skill)
                            all_sprites.add(skill)
                    elif not boss.defeated:  # Phase 2
                        skill = boss.use_sword_cast(player)  # Pass player to sword cast
                        if skill:
                            boss_skills.add(skill)
                            all_sprites.add(skill)
                            
            if event.type == BOSS_PHASE_TRANSITION and boss_spawned:
                for boss in bosses:  # Get the boss from the bosses group
                    if boss.phase == 1 and boss.health <= boss.max_health // 2 and not boss.defeated:
                        boss.transition_to_phase2()
                        
            if event.type == BOSS_DEFEATED and boss_spawned:
                # Handle boss defeat differently depending on mode
                if c_mode == 1:  # Normal mode - return to main menu
                    # Clear boss and skills
                    bosses.empty()
                    boss_skills.empty()
                    
                    # Stop boss timers
                    pygame.time.set_timer(BOSS_DASH, 0)
                    pygame.time.set_timer(BOSS_SKILL_1, 0)
                    
                    game_won = True
                    SoundManager.play_music(grassplain, loops=-1)
                    from Menu.scenes.main_menu_scene import MainMenuScene
                    menu_scene = MainMenuScene(scene_manager.screen, scene_manager)
                    scene_manager.start_scene(menu_scene)
                    return  # Return to main menu
                else:  # Endless mode - continue playing
                    # Clear boss and skills
                    bosses.empty()
                    boss_skills.empty()
                    
                    # Stop boss timers
                    pygame.time.set_timer(BOSS_DASH, 0)
                    pygame.time.set_timer(BOSS_SKILL_1, 0)
                    
                    # Switch back to normal music
                    SoundManager.play_music(grassplain, loops=-1)
                    boss_spawned = False
                    boss_death_time = pygame.time.get_ticks()
                    
                    # Show boss defeated message
                    player.show_boss_defeated_message()
                    player.score += 1000  # Add score for defeating boss in endless mode
                
        # Handle collisions and game over condition
        if not player.is_leveling_up and not is_paused:  # Only process collisions when not leveling up or paused
            items_move_towards_player(player, items_group)
            
            # Check for player death from enemy collisions
            if player_collide_with_enemies(player, enemies, clock):
                # Game over if player died from enemy collision
                if player.current_health <= 0:
                    SoundManager.play_game_over()
                    print(f"[DEBUG] Player died from collision, score: {player.score}")
                    from Menu.scenes.game_over_scene import GameOverScene
                    game_over_scene = GameOverScene(pygame.display.get_surface())
                    game_over_scene.setup(score=player.score)
                    game_over_scene.final_score = player.score  # Direct assignment
                    game_over_scene.score = player.score  # Set base class score too
                    print(f"[DEBUG] Game over scene final_score: {game_over_scene.final_score}")
                    return game_over_scene
                    
            # Handle other collisions
            if player_collide_with_exp_items(player, exp_items):
                pass
            if player_collide_with_energy_items(player, energy_items):
                pass
            if player_collide_with_hp_items(player, hp_items):
                pass
            # Process regular enemies
            for enemy in list(enemies):  # Convert to list for safe iteration
                enemy_died = enemy_collide_with_player_bullets(
                    enemy, player_bullets, exp_items, hp_items, energy_items, 
                    items_group, all_sprites, clock
                )
                if enemy_died:
                    player.score += 10  # Increase score when enemy is killed
                    enemy.kill()  # Remove from all groups
            
            # Process elite enemies
            for elite in list(elites):  # Convert to list for safe iteration
                elite_died, flag = elite_collide_with_player_bullets(elite, player_bullets, clock, flag)
                if elite_died:
                    player.score += 50  # Increase score when elite is killed
                    elite.kill()  # Remove from all groups
                
                # Check for player collision with elite
                if elite_collide_with_player(elites, player, clock, flag):
                    pass  # Handle player collision if needed
            
            # Check for elite bullet collisions with player
            for bullet in list(elite_bullets):
                if pygame.sprite.collide_rect(player, bullet):
                    player.take_damage(bullet.damage)
                    bullet.kill()  # Remove the bullet after hitting the player
                    
            # Handle boss collisions and mechanics
            for boss in bosses:
                # Check for player bullets hitting boss
                for bullet in player_bullets:
                    if pygame.sprite.collide_rect(boss, bullet):
                        if not boss.is_transitioning and not boss.defeated:  # Only take damage if not in transition
                            boss.take_damage(bullet.damage)
                            player.score += 5  # Small score for hitting boss
                            bullet.kill()
                
                # Check for player collision with boss
                if pygame.sprite.collide_rect(boss, player) and not boss.defeated:
                    if pygame.time.get_ticks() - player.damage_time > player.damage_cooldown:
                        player.take_damage(boss.collide_damage)
                        player.damage_time = pygame.time.get_ticks()
                
                # Check for boss defeat
                if boss.defeated and c_mode == 1:  # Normal mode
                    print("[DEBUG] Boss defeated! Showing victory scene...")
                    # Switch to normal music
                    SoundManager.play_music(grassplain, loops=-1)
                    
                    # Return victory scene with player's score
                    print(f"[DEBUG] Boss defeated, returning victory scene, score: {player.score}")
                    from Menu.scenes.victory_scene import VictoryScene
                    victory_scene = VictoryScene(pygame.display.get_surface())
                    victory_scene.setup(score=player.score)
                    victory_scene.score = player.score  # Direct assignment to be sure
                    print(f"[DEBUG] Victory scene score: {victory_scene.score}")
                    return victory_scene
        
        # Update game state
        if not is_paused:
            if not player.is_leveling_up:
                camera.update(player)
                player.update(clock, camera, pressed_keys, player_bullets, all_sprites, background)
                enemies.update(player, player_bullets, all_sprites, clock)
                elites.update(player, elite_bullets, all_sprites, clock)
                
                # Update boss and boss skills
                current_boss_spawned = boss_spawned or game_state.get('boss_spawned', False)
                if current_boss_spawned and bosses:
                    for boss in bosses:
                        if hasattr(boss, 'update'):
                            boss.update(player, player_bullets, all_sprites, clock, boss_skills)
                            
                            # Update feathers if boss is defeated
                            if boss.defeated and hasattr(boss, 'feathers'):
                                for feather in boss.feathers[:]:  # Use a copy for safe iteration
                                    if hasattr(feather, 'update'):
                                        feather.update()
                    
                    if hasattr(boss_skills, 'update'):
                        boss_skills.update(clock)
                        
                # Update all projectiles and items
                player_bullets.update(camera)
                elite_bullets.update(camera)
                exp_items.update()
                energy_items.update()
                hp_items.update()
        
        # Draw everything to the screen
        screen = pygame.display.get_surface()
        screen.fill(Black)
        
        # Draw background
        background.draw(screen, camera)
        
        # Draw boss trail effect if boss is dashing
        current_boss_spawned = boss_spawned or game_state.get('boss_spawned', False)
        if current_boss_spawned and bosses:
            for boss in bosses:
                if (hasattr(boss, 'trail_positions') and 
                    hasattr(boss, 'dash_sprite') and 
                    hasattr(boss, 'defeated') and
                    boss.trail_positions and 
                    not boss.defeated):
                    # Draw each trail position on the screen
                    for trail in boss.trail_positions:
                        if 'x' in trail and 'y' in trail and 'surf' in trail:
                            # Create a rect for the trail image and position it
                            trail_rect = boss.dash_sprite.get_rect(center=(trail['x'], trail['y']))
                            # Apply camera position to the trail position
                            trail_rect.x += camera.camera.x
                            trail_rect.y += camera.camera.y
                            # Draw the trail image
                            screen.blit(trail['surf'], trail_rect)
        
        # Draw elite enemies' trail effects
        for elite in elites:
            if hasattr(elite, 'trail_positions') and elite.trail_positions:
                for trail in elite.trail_positions:
                    # Create a rect for the trail image and position it
                    trail_rect = trail['surf'].get_rect(center=(trail['x'], trail['y']))
                    # Apply camera position to the trail position
                    trail_rect.x += camera.camera.x
                    trail_rect.y += camera.camera.y
                    # Draw the trail image
                    screen.blit(trail['surf'], trail_rect)
        
        # Draw all sprites relative to the camera
        for entity in all_sprites:
            try:
                if hasattr(entity, 'draw'):
                    entity.draw(screen, camera)
                else:
                    screen.blit(entity.surf, camera.apply(entity))
            except Exception as e:
                print(f"Error drawing entity: {e}")
                continue
                
        # No need for victory message here anymore - using VictoryScene instead
                
        # Draw UI elements (health, energy, score, etc.)
        player.advanced_health()
        player.advanced_energy()
        player.advanced_exp()
        
        # Draw score and level first
        player.ui.draw_score_and_level(screen, player.score, player.level)
        
        # Draw game mode indicator below score
        mode_text = player.ui.small_font.render(f"MODE: {'NORMAL' if c_mode == 1 else 'ENDLESS'}", True, (200, 200, 200))
        screen.blit(mode_text, (10, 105))  # Positioned below the level text
        
        # Draw boss health bars if bosses exist
        current_boss_spawned = boss_spawned or game_state.get('boss_spawned', False)
        
        # Initialize boss music state if not exists
        if 'boss_music_playing' not in game_state:
            game_state['boss_music_playing'] = False
            
        if current_boss_spawned and bosses:
            # Draw each boss's health bar with vertical offset
            for i, boss in enumerate(bosses):
                if hasattr(boss, 'health') and hasattr(boss, 'max_health'):
                    # Offset each health bar vertically (50px between them)
                    offset_y = i * 50
                    player.ui.draw_boss_health_bar(screen, boss, offset_y=offset_y)
            
            # Change to boss music if not already playing
            if not game_state['boss_music_playing']:
                SoundManager.play_music(grassplain_boss, loops=-1)
                game_state['boss_music_playing'] = True
        else:
            # Change back to normal music when no bosses
            if game_state['boss_music_playing']:
                SoundManager.play_music(grassplain, loops=-1)
                game_state['boss_music_playing'] = False
            
        # Draw level up menu if leveling up
        if player.is_leveling_up:
            player.ui.draw_level_up_menu(screen, player.available_buffs)
        
        # Draw pause button (only when game is not paused)
        if not is_paused:
            pause_button = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
            pygame.draw.rect(screen, (100, 100, 100), pause_button)
            pygame.draw.rect(screen, (200, 200, 200), pause_button, 2)
            pause_text = player.ui.font.render("II", True, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=pause_button.center)
            screen.blit(pause_text, pause_text_rect)
        
        # Draw pause menu or help screen if game is paused
        if is_paused:
            if show_help:
                # Draw help screen
                player.ui.draw_pause_menu(screen, player, show_help=True)
            else:
                # Draw regular pause menu
                player.ui.draw_pause_menu(screen, player, show_help=False)
        
        # Draw custom cursor for better UX when not in level up menu
        if not player.is_leveling_up:
            mouse_pos = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)  # Hide default cursor
            # Draw crosshair cursor
            pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 10, 1)
            pygame.draw.line(screen, (255, 255, 255), (mouse_pos[0]-5, mouse_pos[1]), (mouse_pos[0]+5, mouse_pos[1]), 1)
            pygame.draw.line(screen, (255, 255, 255), (mouse_pos[0], mouse_pos[1]-5), (mouse_pos[0], mouse_pos[1]+5), 1)
        else:
            pygame.mouse.set_visible(True)  # Show default cursor in level up menu
        
        # Check if player is dead
        if player.current_health <= 0:
            # Play game over sound
            SoundManager.play_game_over()
            
            # Stop background music
            pygame.mixer.music.fadeout(1000)
            
            # Hủy tất cả các timer
            reset_timer()
            
            # Debug print score before transition
            print(f"[DEBUG] Player score at game over: {player.score}")
            
            # Transition to the Game Over scene with player's score
            from Menu.scenes.game_over_scene import GameOverScene
            
            # Create the game over scene
            game_over_scene = GameOverScene(pygame.display.get_surface())
            
            # Set up the scene with the score
            game_over_scene.setup(score=player.score)
            game_over_scene.final_score = player.score
            game_over_scene.score = player.score
            
            print(f"[DEBUG] Game over scene final_score: {game_over_scene.final_score}")
            
            # Return the scene to be handled by the GameScene
            return game_over_scene
        
        # Draw exp bar
        player.advanced_exp()
        
        # Draw victory message if player won in normal mode
        if game_won:
            # Hủy tất cả các timer
            reset_timer()
            
            # Debug print score before transition
            print(f"[DEBUG] Player score at victory: {player.score}")
            
            # Transition to Victory scene with player's score
            from Menu.scenes.victory_scene import VictoryScene
            victory_scene = VictoryScene(pygame.display.get_surface())
            
            # Manually set score in a way that ensures it gets displayed
            victory_scene.setup(score=player.score)  # Pass the player's score
            victory_scene.score = player.score  # Direct assignment to be sure
            
            # Debug final score value
            print(f"[DEBUG] Victory scene score: {victory_scene.score}")
            
            # If scene_manager is available, use it for the transition
            if scene_manager:
                # Debug scene_manager
                print(f"[DEBUG] Using scene_manager to change to victory scene")
                scene_manager.change_scene('victory', player.score)
                return None
            else:
                # Debug direct return
                print(f"[DEBUG] Returning victory_scene directly")
                # Return the scene directly if no scene manager
                return victory_scene
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    Run_Game()