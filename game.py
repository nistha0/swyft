"""
SWYFT - Main Game Loop with Ready State
"""
import pygame
import config
from terrain import Terrain
from entities import Cloud
from car import Car
from camera import Camera
from physics import PhysicsEngine
from game_state import GameState
from renderer import Renderer
from input_handler import InputHandler
from music_manager import get_music_manager

def run_game(control_mode="buttons"):
    """Main game function"""
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("SWYFT - Hill Climb Racing")
    clock = pygame.time.Clock()
    
    music_manager = get_music_manager()
    
    # Gesture handler
    gesture_handler = None
    actual_control_mode = control_mode
    
    if control_mode == "gestures":
        try:
            print("\n" + "="*60)
            print("INITIALIZING GESTURE CONTROL")
            print("="*60)
            
            from gesture_handler import GestureHandler
            gesture_handler = GestureHandler()
            
            if gesture_handler.available:
                print("\n→ Starting camera and hand tracking...")
                if gesture_handler.start():
                    print("\n" + "✓"*30)
                    print("GESTURE CONTROL ACTIVE!")
                    print("✓"*30)
                    print("\nCamera feed will appear in the bottom-right corner of the game")
                    print("Show your hand to control the car!\n")
                else:
                    print("\n" + "✗"*30)
                    print("CAMERA FAILED TO START")
                    print("✗"*30)
                    print("\n→ Falling back to keyboard controls")
                    print("  Use arrow keys or WASD to play\n")
                    gesture_handler = None
                    actual_control_mode = "buttons"
            else:
                print("\n" + "✗"*30)
                print("GESTURE DEPENDENCIES NOT AVAILABLE")
                print("✗"*30)
                print("\n→ Falling back to keyboard controls")
                print("  Install dependencies: pip install opencv-python mediapipe==0.10.7\n")
                gesture_handler = None
                actual_control_mode = "buttons"
                
        except Exception as e:
            print(f"\n✗ Error initializing gesture control: {e}")
            print("→ Falling back to keyboard controls\n")
            gesture_handler = None
            actual_control_mode = "buttons"
    
    game_running = True
    
    while game_running:
        terrain = Terrain()
        car = Car(400.0, 0.0)
        camera = Camera()
        physics = PhysicsEngine()
        game_state = GameState(terrain, actual_control_mode)  # Pass control mode
        renderer = Renderer(screen)
        input_handler = InputHandler(gesture_handler)
        clouds = [Cloud() for _ in range(config.NUM_CLOUDS)]
        
        car.align_to_ground(terrain.get_height_at(car.x))
        
        running = True
        game_over = False
        paused = False
        ready_state = True  # Game starts in ready state
        
        while running:
            dt = clock.tick(config.FPS) / 1000
            
            # ALWAYS handle events
            input_handler.handle_events()
            
            if input_handler.should_quit():
                if gesture_handler:
                    gesture_handler.stop()
                return "quit"
            
            # Handle ready state
            if ready_state:
                # IMPORTANT: Update input state even in ready mode
                input_handler.update_input()
                
                # Update clouds for visual effect
                for cloud in clouds:
                    cloud.update(dt)
                
                # Render the scene with ready message
                mouse_pos = input_handler.get_mouse_pos()
                gesture_frame = gesture_handler.get_frame() if gesture_handler else None
                renderer.render_scene(
                    clouds, terrain, game_state.get_coins(), game_state.get_fuel_canisters(),
                    car, camera.get_x(), game_state.get_score_data(), game_state.game_time,
                    game_over=False, mouse_pos=mouse_pos,
                    is_sound_on=music_manager.is_music_enabled(),
                    gesture_frame=gesture_frame,
                    ready_state=True,
                    control_mode=actual_control_mode
                )
                
                # Check if player is ready to start
                if gesture_handler and gesture_handler.is_active():
                    # For gesture control, start when hand is detected and making a gesture
                    if gesture_handler.is_accelerating() or gesture_handler.is_braking():
                        ready_state = False
                        print("\n✓ Game started! Hand gesture detected.\n")
                else:
                    # For keyboard, start on any acceleration or brake key
                    if input_handler.is_accelerating() or input_handler.is_braking():
                        ready_state = False
                        print("\n✓ Game started!\n")
                
                continue
            
            if input_handler.should_pause() and not game_over:
                paused = not paused
                if paused:
                    music_manager.pause_music()
                else:
                    music_manager.unpause_music()
            
            # Auto-pause when no hand detected in gesture mode
            if control_mode == "gestures" and gesture_handler and not game_over and not ready_state:
                if not gesture_handler.has_hand_detected() and not paused:
                    paused = True
                    music_manager.pause_music()
                    print("⚠ No hand detected - Game paused")
            
            if game_over:
                if input_handler.should_restart():
                    break
                if input_handler.should_go_to_menu():
                    if gesture_handler:
                        gesture_handler.stop()
                    return "menu"
                
                renderer.render_scene(
                    clouds, terrain, game_state.get_coins(), game_state.get_fuel_canisters(),
                    car, camera.get_x(), game_state.get_score_data(), game_state.game_time,
                    game_over=True, death_reason=game_state.get_death_reason(),
                    is_sound_on=music_manager.is_music_enabled()
                )
                
                if input_handler.was_pause_button_clicked():
                    mouse_pos = input_handler.get_mouse_pos()
                    _, _, _, sound_button_rect = renderer.render_scene(
                        clouds, terrain, game_state.get_coins(), game_state.get_fuel_canisters(),
                        car, camera.get_x(), game_state.get_score_data(), game_state.game_time,
                        game_over=True, death_reason=game_state.get_death_reason(),
                        is_sound_on=music_manager.is_music_enabled()
                    )
                    if sound_button_rect and sound_button_rect.collidepoint(mouse_pos):
                        music_manager.toggle_music()
                        if music_manager.is_music_enabled():
                            music_manager.play_gameplay_music()
                continue
            
            if paused:
                # Allow P key to unpause as well
                if input_handler.should_pause():
                    paused = False
                    music_manager.unpause_music()
                    continue
                
                mouse_pos = input_handler.get_mouse_pos()
                pause_button_rect, resume_rect, menu_rect, sound_button_rect = renderer.render_scene(
                    clouds, terrain, game_state.get_coins(), game_state.get_fuel_canisters(),
                    car, camera.get_x(), game_state.get_score_data(), game_state.game_time,
                    paused=True, mouse_pos=mouse_pos, is_sound_on=music_manager.is_music_enabled()
                )
                
                if input_handler.was_pause_button_clicked():
                    if resume_rect and resume_rect.collidepoint(mouse_pos):
                        paused = False
                        music_manager.unpause_music()
                    elif menu_rect and menu_rect.collidepoint(mouse_pos):
                        if gesture_handler:
                            gesture_handler.stop()
                        return "menu"
                    elif sound_button_rect and sound_button_rect.collidepoint(mouse_pos):
                        music_manager.toggle_music()
                        if music_manager.is_music_enabled():
                            music_manager.unpause_music()
                continue
            
            # Update input for normal gameplay
            input_handler.update_input()
            
            car_x, car_y = car.get_position()
            ground_y = terrain.get_height_at(car_x)
            ground_angle = terrain.get_angle_at(car_x)
            on_ground = car_y >= ground_y - car.get_height() / 2 + config.CAR_GROUND_OFFSET
            
            if on_ground:
                car.align_to_ground(ground_y)
                physics.reset_vertical_velocity()
                
                # Get speed multiplier for gesture controls
                speed_multiplier = 1.0
                if control_mode == "gestures" and gesture_handler:
                    speed_multiplier = gesture_handler.get_speed_multiplier()
                
                if input_handler.is_accelerating():
                    physics.accelerate(dt, speed_multiplier)
                if input_handler.is_braking():
                    physics.brake(dt)
                
                physics.apply_ground_friction()
            else:
                physics.apply_gravity(dt)
                physics.apply_air_friction()
            
            physics.clamp_velocity()
            
            vel_x, vel_y = physics.get_velocity()
            
            # Update rotation with speed-based tilt
            car.update_rotation(ground_angle, dt, vel_x)
            
            car.update_position(vel_x, vel_y, dt)
            
            car_x, car_y = car.get_position()
            camera.follow(car_x, dt)
            camera_x = camera.get_x()
            
            game_state.update(dt, car_x, car_y, camera_x, input_handler.is_accelerating(), car.rotation, vel_x)
            
            if game_state.is_game_over():
                game_over = True
            
            for cloud in clouds:
                cloud.update(dt)
            
            if car_x > terrain.points[-1][0] - 1500:
                terrain.extend_terrain()
            
            mouse_pos = input_handler.get_mouse_pos()
            gesture_frame = gesture_handler.get_frame() if gesture_handler else None
            pause_button_rect, _, _, sound_button_rect = renderer.render_scene(
                clouds, terrain, game_state.get_coins(), game_state.get_fuel_canisters(),
                car, camera_x, game_state.get_score_data(), game_state.game_time,
                game_over=game_over, mouse_pos=mouse_pos,
                is_sound_on=music_manager.is_music_enabled(),
                gesture_frame=gesture_frame
            )
            
            if input_handler.was_pause_button_clicked():
                if pause_button_rect and pause_button_rect.collidepoint(mouse_pos):
                    paused = True
                elif sound_button_rect and sound_button_rect.collidepoint(mouse_pos):
                    music_manager.toggle_music()
                    if music_manager.is_music_enabled():
                        music_manager.play_gameplay_music()
    
    if gesture_handler:
        gesture_handler.stop()
    
    pygame.quit()
    return "menu"

if __name__ == "__main__":
    run_game()
