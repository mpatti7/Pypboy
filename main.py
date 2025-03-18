import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from controllers.home import HomeController
import os
from components.luck_manager import LuckManager
import RPi.GPIO as GPIO

# os.environ['SDL_AUDIODRIVER'] = 'pipewire'
# os.environ["SDL_FBDEV"] = "/dev/fb0"
# os.environ["SDL_AUDIODRIVER"] = "dummy"

ROTARY_POSITIONS = {
    4: "Stats",
    17: "Map",
    27: "Weather",
    23: "Game",
    22: "Radio"
}

ROTARY_SWITCH_EVENT = pygame.USEREVENT + 1


class PipboyApp:
    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((720, 480), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption("Pipboy 3000")
        self.clock = pygame.time.Clock()
        
        info = pygame.display.Info()
        print(f"Detected screen resolution: {info.current_w}x{info.current_h}") 
        
        # Initialize the current screen (default: Home Screen)
        self.current_controller = HomeController(self.screen, ROTARY_SWITCH_EVENT)
        luck = LuckManager()
        luck.generate_time_ranges()

        GPIO.setmode(GPIO.BCM)
        for pin in ROTARY_POSITIONS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.last_rotary_position = None
    

    def check_rotary_switch(self):
        """Check rotary switch position and post a Pygame event if it changes."""
        for pin, view_name in ROTARY_POSITIONS.items():
            if GPIO.input(pin) == GPIO.LOW:  # If the switch is at this position
                if view_name != self.last_rotary_position:
                    pygame.event.post(pygame.event.Event(ROTARY_SWITCH_EVENT, {"view_name": view_name}))
                    self.last_rotary_position = view_name
                break


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                
                if event.type == ROTARY_SWITCH_EVENT:
                    self.current_controller.handle_event(event)

                # Pass events to the current screen controller
                self.current_controller.handle_event(event)

            # Update the current screen
            self.current_controller.update()

            # Render the current screen
            self.current_controller.render()

            pygame.display.flip()
            self.clock.tick(FPS)
            self.check_rotary_switch()

        pygame.quit()
        GPIO.cleanup()


if __name__ == "__main__":
    app = PipboyApp()
    app.run()
