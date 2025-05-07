import pygame
pygame.init()

class Screen:
    def __init__(self):
        pass

    def window_screen(self):
        # Get screen info and set up display
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Set window size to 80% of screen size
        self.window_width = int(self.screen_width * 0.8)
        self.window_height = int(self.screen_height * 0.8)
        
        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Card Game")
        self.running = True

        self.card_resize()

    def card_resize(self):
        # Calculate card size based on window size (smaller cards)
        self.card_width = int(self.window_width * 0.08)  # 8% of window width (reduced from 15%)
        self.card_height = int(self.card_width * 1.5)    # 1.5 times width for aspect ratio
        self.font = pygame.font.Font(None, int(self.window_height * 0.04))  # Scale font size


    async def handle_input(self, writer):
        for event in pygame.event.get():
            self.screen.fill((0,0,255))
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event)

    def stop():
        pygame.quit()