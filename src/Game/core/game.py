import pygame
import random
import sys

sys.path.insert(0, r"./src/Menu")

# Import from our reorganized modules
from ..core.define import *
from ..core.camera import *
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
from ..managers.sound_manager import SoundManager, grassplain, grassplain_boss

# Import VictoryScene from Menu.scenes
from Menu.scenes.victory_scene import VictoryScene

pygame.mixer.init()
pygame.init()


def Run_Game(current_mode = 0, character_select = 0):    
    clock = pygame.time.Clock()
    pygame.display.set_caption('A 2D NORMAL SHOOTING GAME')
    SoundManager.play_music(grassplain, loops=-1)
    

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
    
    # Tạo ra 1 object
    camera = Camera(LEVEL_WIDTH, LEVEL_HEIGHT)
    
    if character_select == 1:
        player = Player_Male()
    else:
        player = Player_Female()
    all_sprites.add(player)

    enemy = Normal(player)
    enemy_new_speed = enemy.get_speed()
    enemy_new_hp = enemy.get_hp()
    enemy_new_damage = enemy.get_damage()
    background = Background(background_sprite)
    
    # Boss related variables
    boss_spawned = False
    boss_death_time = 0
    boss_respawn_time = 300000  # 5 minutes (in milliseconds)
    
    flag = 0
    c_mode = current_mode
    is_paused = False  # Thêm biến để kiểm tra trạng thái pause
    game_won = False   # Flag to check if player won the game in normal mode
    
    # Reset game state and set boss spawn timer based on game mode
    game_won = False
    victory_time = 0
    victory_delay = 5000  # 5 seconds delay before returning to menu
    
    if c_mode == 1:  # Normal mode (1 = Normal, 0 = Endless)
        print("[DEBUG] Setting up NORMAL mode - boss will spawn in 30 seconds")
        pygame.time.set_timer(ADD_BOSS, 3000)  # 30 seconds for normal mode
    else:  # Endless mode
        print("[DEBUG] Setting up ENDLESS mode - boss will spawn in 5 minutes")
        pygame.time.set_timer(ADD_BOSS, 3000)  # 5 minutes for endless mode
    
    # Gameplay chạy trong này
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()
        SCREEN.fill(Black)            

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Handle keyboard events
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_p:  # Toggle pause with P key
                    is_paused = not is_paused
                    if is_paused:
                        # Play pause sound and show menu
                        SoundManager.play_pause_game()
                        # The menu will be drawn in the main loop
                elif event.key == K_q and player.energy >= player.maximum_energy and player.burst_clock < player.burst_time and not is_paused and not player.is_leveling_up:
                    player.energy = 0
                    player.burst = True
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if is_paused:
                    # Handle pause menu button clicks
                    if hasattr(player.ui, 'resume_rect') and player.ui.resume_rect.collidepoint(mouse_pos):
                        SoundManager.play_button_select()
                        is_paused = False
                    elif hasattr(player.ui, 'menu_rect') and player.ui.menu_rect.collidepoint(mouse_pos):
                        SoundManager.play_button_select()
                        SoundManager.play_button_select()
                        pygame.mouse.set_visible(True)  # Make sure cursor is visible when returning to menu
                        return  # Return to main menu
                
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
                
            # Các sự kiện của Enemy
            if event.type == ADD_ENEMY and not player.is_leveling_up and not is_paused:  # Không tạo enemy khi đang level up hoặc pause
                for _ in range(20):  # Tạo 20 kẻ địch
                    new_enemy = Normal(player)
                    new_enemy.set_speed(enemy_new_speed)
                    new_enemy.set_hp(enemy_new_hp)
                    new_enemy.set_damage(enemy_new_damage)
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                    
            if event.type == INCREASE_STAT and not is_paused:
                enemy_new_speed += 1
                enemy_new_hp += 10
                enemy_new_damage += 10
                 
            # Các sự kiện của enemy Elite
            if event.type == ADD_ELITE and not player.is_leveling_up and not is_paused:  # Không tạo elite khi đang level up hoặc pause
                rand = random.randint(1, 4)
                if rand == 1:
                    new_elite = Elite_1(player)
                elif rand == 2:
                    new_elite = Elite_2(player)
                elif rand == 3:
                    new_elite = Elite_3(player)
                else:
                    new_elite = Elite_4(player)
                elites.add(new_elite)
                all_sprites.add(new_elite)
                
            # Handle boss events
            if event.type == ADD_BOSS and not is_paused and not player.is_leveling_up and not boss_spawned:
                print(f"[DEBUG] ADD_BOSS event triggered. Mode: {'NORMAL' if c_mode == 0 else 'ENDLESS'}, Game won: {game_won}, Time since death: {pygame.time.get_ticks() - boss_death_time}ms")
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
                    return MainMenuScene(pygame.display.get_surface())
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
                    from Menu.scenes.game_over_scene import GameOverScene
                    game_over_scene = GameOverScene(pygame.display.get_surface())
                    game_over_scene.setup(score=player.score)
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
                    from Menu.scenes.victory_scene import VictoryScene
                    victory_scene = VictoryScene(pygame.display.get_surface())
                    victory_scene.setup(score=player.score)
                    return victory_scene
        
        # Update game state
        if not is_paused:
            if not player.is_leveling_up:
                camera.update(player)
                player.update(clock, camera, pressed_keys, player_bullets, all_sprites, background)
                enemies.update(player, player_bullets, all_sprites, clock)
                elites.update(player, elite_bullets, all_sprites, clock)
                
                # Update boss and boss skills
                if boss_spawned:
                    for boss in bosses:
                        boss.update(player, player_bullets, all_sprites, clock, boss_skills)
                        
                        # Update feathers if boss is defeated
                        if boss.defeated and hasattr(boss, 'feathers'):
                            for feather in boss.feathers[:]:  # Use a copy for safe iteration
                                if hasattr(feather, 'update'):
                                    feather.update()
                    
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
        if boss_spawned:
            for boss in bosses:
                if hasattr(boss, 'trail_positions') and boss.trail_positions and not boss.defeated:
                    # Draw each trail position on the screen
                    for trail in boss.trail_positions:
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
        
        # Draw game mode indicator
        mode_text = player.ui.font.render("MODE: NORMAL" if c_mode == 1 else "MODE: ENDLESS", True, (255, 255, 255))
        screen.blit(mode_text, (10, 10))
        
        player.ui.draw_score_and_level(screen, player.score, player.level)
        player.ui.draw_stats(screen, player)
        
        # Draw boss health bar if boss exists
        if boss_spawned:
            for boss in bosses:
                player.ui.draw_boss_health_bar(screen, boss)
            
        # Draw level up menu if leveling up
        if player.is_leveling_up:
            player.ui.draw_level_up_menu(screen, player.available_buffs)
        
        # Draw pause button (only show when game is not paused or leveling up)
        if not is_paused and not player.is_leveling_up:
            pause_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
            pygame.draw.rect(screen, (100, 100, 100), pause_rect)
            pygame.draw.rect(screen, (200, 200, 200), pause_rect, 2)
            pause_text = player.ui.small_font.render("II", True, (255, 255, 255))
            screen.blit(pause_text, (SCREEN_WIDTH - 40, 20))
        
        # Draw pause menu if game is paused
        if is_paused and not player.is_leveling_up:
            # Draw the pause menu and get button rectangles
            pause_menu_buttons = player.ui.draw_pause_menu(screen)
            
            # Draw custom cursor for better UX
            mouse_pos = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)  # Hide default cursor
            pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 10, 1)
            pygame.draw.line(screen, (255, 255, 255), (mouse_pos[0]-5, mouse_pos[1]), (mouse_pos[0]+5, mouse_pos[1]), 1)
            pygame.draw.line(screen, (255, 255, 255), (mouse_pos[0], mouse_pos[1]-5), (mouse_pos[0], mouse_pos[1]+5), 1)
        else:
            pygame.mouse.set_visible(True)  # Show default cursor when not paused
        
        # Check if player is dead
        if player.current_health <= 0:
            # Play game over sound
            SoundManager.play_game_over()
            
            # Stop background music
            pygame.mixer.music.fadeout(1000)
            
            # Display game over screen
            game_over_text = player.ui.big_font.render("GAME OVER", True, (255, 0, 0))
            score_text = player.ui.font.render(f"Final Score: {player.score}", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)
            pygame.display.flip()
            pygame.time.delay(3000)  # Show game over for 3 seconds
            
            # Return to main menu
            from Menu.scenes.main_menu_scene import MainMenuScene
            return MainMenuScene(pygame.display.get_surface())
        
        # Draw exp bar
        player.advanced_exp()
        
        # Draw victory message if player won in normal mode
        if game_won:
            victory_text = player.ui.title_font.render("VICTORY!", True, (255, 215, 0))
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(victory_text, victory_rect)
            
            continue_text = player.ui.font.render("Press any key to continue", True, (255, 255, 255))
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(continue_text, continue_rect)
            
            pygame.display.flip()
            
            # Wait for any key press
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        return  # Return to main menu
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    Run_Game()