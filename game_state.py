"""
SWYFT - Game State Manager with Difficulty Support
Manages game state, score, fuel, and collectible spawning based on difficulty
"""
import random
import config
from entities import Coin, FuelCanister

class GameState:
    def __init__(self, terrain, control_mode="buttons"):
        self.coins_collected = 0
        self.distance = 0
        self.game_time = 0
        self.terrain = terrain
        self.fuel = config.FUEL_INITIAL
        self.is_dead = False
        self.death_reason = ""
        self.control_mode = control_mode  # Store control mode
        
        # Get difficulty settings FIRST (before loading high score)
        self.difficulty = getattr(config, 'DIFFICULTY', 'MEDIUM')
        
        # Now load high score for this difficulty
        self.high_score = self._load_high_score()
        
        # Smooth fuel refill system
        self.fuel_refill_animation = 0  # Timer for refill animation
        self.target_fuel = self.fuel  # Target fuel for smooth interpolation
        
        # Apply difficulty settings
        self._apply_difficulty_settings()
        
        # Coin management
        self.coins = []
        self.next_coin_spawn = 600
        
        # Fuel canister management
        self.fuel_canisters = []
        self.next_fuel_spawn = 800

    def _apply_difficulty_settings(self):
        """Apply difficulty-specific settings with control mode consideration"""
        if self.difficulty in config.DIFFICULTY_SETTINGS:
            settings = config.DIFFICULTY_SETTINGS[self.difficulty]
            self.max_tilt_angle = settings['MAX_TILT_ANGLE']
            
            # Use gesture-specific fuel rates if in gesture mode
            if self.control_mode == "gestures":
                self.fuel_consumption_rate = settings.get('GESTURE_FUEL_CONSUMPTION', settings['FUEL_CONSUMPTION_RATE'])
                self.fuel_idle_consumption = settings.get('GESTURE_FUEL_IDLE', settings['FUEL_IDLE_CONSUMPTION'])
            else:
                self.fuel_consumption_rate = settings['FUEL_CONSUMPTION_RATE']
                self.fuel_idle_consumption = settings['FUEL_IDLE_CONSUMPTION']
            
            self.coin_frequency = settings['COIN_SPAWN_FREQUENCY']
        else:
            # Defaults
            self.max_tilt_angle = config.CAR_MAX_TILT_ANGLE
            self.fuel_consumption_rate = config.FUEL_CONSUMPTION_RATE
            self.fuel_idle_consumption = config.FUEL_IDLE_CONSUMPTION
            self.coin_frequency = 1.0

    def _load_high_score(self):
        """Load difficulty-specific high score from file"""
        # Get difficulty at init time and store it
        if not hasattr(self, 'difficulty'):
            self.difficulty = getattr(config, 'DIFFICULTY', 'MEDIUM')
        filename = f"highscore_{self.difficulty.lower()}.txt"
        try:
            with open(filename, "r") as f:
                score = int(float(f.read().strip()))
                print(f"[DEBUG] Loaded high score for {self.difficulty}: {score}")
                return score
        except (FileNotFoundError, ValueError) as e:
            print(f"[DEBUG] No high score file for {self.difficulty}, starting at 0")
            return 0
    
    def _save_high_score(self):
        """Save difficulty-specific high score to file"""
        filename = f"highscore_{self.difficulty.lower()}.txt"
        try:
            with open(filename, "w") as f:
                f.write(str(int(self.high_score)))
            print(f"[DEBUG] Saved high score for {self.difficulty}: {int(self.high_score)} to {filename}")
        except Exception as e:
            print(f"[DEBUG] Failed to save high score: {e}")

    def _handle_death(self, reason):
        """Handle player death and high score"""
        self.is_dead = True
        self.death_reason = reason
        
        current_distance = int(self.distance)
        if current_distance >= self.high_score:  # Changed from > to >= to update on tie
            self.high_score = current_distance
            self._save_high_score()
    
    def update(self, dt, car_x, car_y, camera_x, is_accelerating, car_rotation, velocity_x=0):
        """Update game state with aggressive fuel physics"""
        if self.is_dead:
            return
        
        self.game_time += dt
        
        # Update distance
        self.distance = max(self.distance, (car_x - 400) / 50)
        
        # AGGRESSIVE fuel consumption - always draining
        if is_accelerating:
            # Heavy drain when accelerating
            consumption = self.fuel_consumption_rate * dt
        else:
            # Still significant drain even when coasting
            consumption = self.fuel_idle_consumption * dt
        
        # Apply fuel drain
        self.fuel -= consumption
        
        # Clamp fuel
        self.fuel = max(0, min(config.FUEL_INITIAL, self.fuel))
        
        # Check if dead from fuel
        if self.fuel <= 0:
            self._handle_death("Out of Fuel!")
            return
        
        # Check if dead from flipping (difficulty-based with slope consideration)
        if config.CAR_FLIP_DEATH_ENABLED:
            abs_rotation = abs(car_rotation)
            # Normalize rotation to 0-180 range
            while abs_rotation > 180:
                abs_rotation -= 360
            abs_rotation = abs(abs_rotation)
            
            # Get terrain angle to detect steep slopes
            terrain_angle = abs(self.terrain.get_angle_at(car_x))
            
            # On steep slopes, car is more likely to flip
            slope_penalty = 0
            if terrain_angle > 25:  # Steep slope
                slope_penalty = 15  # Reduce flip tolerance by 15 degrees
            elif terrain_angle > 15:  # Moderate slope
                slope_penalty = 8  # Reduce flip tolerance by 8 degrees
            
            effective_max_tilt = self.max_tilt_angle - slope_penalty
            
            if abs_rotation > effective_max_tilt:
                if terrain_angle > 25:
                    self._handle_death("Crashed on Steep Slope!")
                else:
                    self._handle_death("Car Flipped!")
                return
        
        # Extra strict mode for HARD difficulty on dangerous terrain
        if self.difficulty == "HARD":
            terrain_angle = abs(self.terrain.get_angle_at(car_x))
            abs_rotation = abs(car_rotation)
            while abs_rotation > 180:
                abs_rotation -= 360
            abs_rotation = abs(abs_rotation)
            
            # On very steep slopes in hard mode, even less tolerance
            if terrain_angle > 30 and abs_rotation > 50:
                self._handle_death("Extreme Slope Crash!")
                return
        
        # Update coins
        for coin in self.coins:
            coin.update(dt, self.game_time)
            if coin.check_collision(car_x, car_y):
                self.coins_collected += 1
        
        # Update fuel canisters with smooth refill
        for fuel_can in self.fuel_canisters:
            fuel_can.update(dt, self.game_time)
            if fuel_can.check_collision(car_x, car_y):
                # Smooth refill: set target and animate
                self.target_fuel = min(config.FUEL_INITIAL, self.fuel + config.FUEL_REFILL_AMOUNT)
                self.fuel_refill_animation = 0.5  # 0.5 second refill animation
        
        # Smooth fuel refill animation (like modern racing games)
        if self.fuel_refill_animation > 0:
            self.fuel_refill_animation -= dt
            # Smooth interpolation towards target
            refill_speed = 120  # Fuel units per second during refill
            if self.fuel < self.target_fuel:
                self.fuel = min(self.target_fuel, self.fuel + refill_speed * dt)
        else:
            self.target_fuel = self.fuel
        
        # Spawn new coins
        self._spawn_coins(camera_x)
        
        # Spawn new fuel canisters
        self._spawn_fuel(camera_x, car_x)
        
        # Remove off-screen items
        self.coins[:] = [c for c in self.coins if c.x > camera_x - 200]
        self.fuel_canisters[:] = [f for f in self.fuel_canisters if f.x > camera_x - 200]
    
    def _spawn_coins(self, camera_x):
        """Spawn coins ahead of camera (difficulty-adjusted frequency)"""
        while self.next_coin_spawn < camera_x + config.WIDTH + 400:
            cx = self.next_coin_spawn
            cy = self.terrain.get_height_at(cx) - config.COIN_HEIGHT_ABOVE_GROUND
            self.coins.append(Coin(cx, cy))
            
            # Adjust spawn distance based on difficulty
            base_min = int(config.COIN_SPAWN_MIN_DISTANCE * self.coin_frequency)
            base_max = int(config.COIN_SPAWN_MAX_DISTANCE * self.coin_frequency)
            
            self.next_coin_spawn += random.randint(base_min, base_max)
    
    def _spawn_fuel(self, camera_x, car_x):
        """Spawn fuel canisters ahead of camera with intelligent placement"""
        while self.next_fuel_spawn < camera_x + config.WIDTH + 400:
            fx = self.next_fuel_spawn
            fy = self.terrain.get_height_at(fx) - config.FUEL_HEIGHT_ABOVE_GROUND
            self.fuel_canisters.append(FuelCanister(fx, fy))
            
            # Dynamic spacing: place fuel closer when player has low fuel
            fuel_percentage = self.fuel / config.FUEL_INITIAL
            if fuel_percentage < 0.3:
                # Critical fuel - spawn closer
                spawn_distance = random.randint(250, 350)
            elif fuel_percentage < 0.5:
                # Low fuel - spawn moderately close
                spawn_distance = random.randint(350, 450)
            else:
                # Good fuel - normal spacing (adjusted by difficulty)
                base_min = config.FUEL_SPAWN_MIN_DISTANCE
                base_max = config.FUEL_SPAWN_MAX_DISTANCE
                
                # Make fuel scarcer in harder difficulties
                if self.difficulty == "HARD":
                    base_min = int(base_min * 1.3)
                    base_max = int(base_max * 1.3)
                elif self.difficulty == "EASY":
                    base_min = int(base_min * 0.8)
                    base_max = int(base_max * 0.8)
                
                spawn_distance = random.randint(base_min, base_max)
            
            self.next_fuel_spawn += spawn_distance
    
    def get_coins(self):
        """Get list of active coins"""
        return self.coins
    
    def get_fuel_canisters(self):
        """Get list of active fuel canisters"""
        return self.fuel_canisters
    
    def get_score_data(self):
        """Get current score data"""
        return {
            'coins': self.coins_collected,
            'distance': int(self.distance),
            'fuel': self.fuel,
            'high_score': self.high_score,
            'is_refilling': self.fuel_refill_animation > 0
        }
    
    def is_game_over(self):
        """Check if game is over"""
        return self.is_dead
    
    def get_death_reason(self):
        """Get the reason for death"""
        return self.death_reason
