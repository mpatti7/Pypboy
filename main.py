import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from controllers.home import HomeController
import os
from components.luck_manager import LuckManager

# os.environ['SDL_AUDIODRIVER'] = 'pipewire'
os.environ["SDL_FBDEV"] = "/dev/fb0"

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
        self.current_controller = HomeController(self.screen)
        luck = LuckManager()
        luck.generate_time_ranges()


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                # Pass events to the current screen controller
                self.current_controller.handle_event(event)

            # Update the current screen
            self.current_controller.update()

            # Render the current screen
            self.current_controller.render()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    app = PipboyApp()
    app.run()
