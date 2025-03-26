import asyncio
import time
import pygame
import json
from pathlib import Path

pygame.init()

class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.player_number = None
        self.current_player = 1
        self.drawn_cards = {}  # Store drawn cards for both players
        self.last_draw_time = 0  # For animation
        self.draw_animation_duration = 500  # milliseconds
        
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
        
        # Calculate card size based on window size (smaller cards)
        self.card_width = int(self.window_width * 0.08)  # 8% of window width (reduced from 15%)
        self.card_height = int(self.card_width * 1.5)    # 1.5 times width for aspect ratio
        
        self.font = pygame.font.Font(None, int(self.window_height * 0.04))  # Scale font size
        self.running = True
        self.images_path = Path(__file__).parent.parent / 'images'
        print(f"Client images path: {self.images_path}")
        print(f"Images path exists: {self.images_path.exists()}")
        print(f"Images path absolute: {self.images_path.absolute()}")
        
        # Check if images directory exists and has files
        if not self.images_path.exists():
            print(f"ERROR: Images directory not found at {self.images_path}")
        else:
            available_images = list(self.images_path.glob('*.png'))
            print(f"Available images in directory: {[f.name for f in available_images]}")
            for img in available_images:
                print(f"Image {img.name} exists: {img.exists()}")
                print(f"Image {img.name} is file: {img.is_file()}")
                print(f"Image {img.name} full path: {img.absolute()}")

    def handle_resize(self, event):
        """Handle window resize events"""
        self.window_width = event.w
        self.window_height = event.h
        self.card_width = int(self.window_width * 0.08)  # 8% of window width
        self.card_height = int(self.card_width * 1.5)
        self.font = pygame.font.Font(None, int(self.window_height * 0.04))

    async def handle_server_message(self, message):
        print(f"Received message: {message}")
        try:
            data = json.loads(message)
            if data["type"] == "card_drawn":
                player = data["player"]
                card = data["card"]
                print(f"Received card data: {card}")
                print(f"Card art path: {self.images_path / card['art']}")
                print(f"Card art exists: {(self.images_path / card['art']).exists()}")
                
                # Store the card data
                self.drawn_cards[player] = card
                self.last_draw_time = pygame.time.get_ticks()  # Start animation
                print(f"Card drawn for player {player}: {card}")
                print(f"Current drawn cards: {self.drawn_cards}")
                
                # Test load the image immediately
                try:
                    image_path = self.images_path / card["art"]
                    if image_path.exists():
                        test_image = pygame.image.load(str(image_path))
                        print(f"Successfully loaded test image: {test_image.get_size()}")
                    else:
                        print(f"ERROR: Image file not found at {image_path}")
                except Exception as e:
                    print(f"Error testing image load: {e}")
                    
            elif data["type"] == "turn_change":
                self.current_player = data["current_player"]
                print(f"Turn changed to player {self.current_player}")
        except json.JSONDecodeError:
            if message == "Game started":
                print("Game has started!")
            elif(message == "Not Player"):
                print("Player disconnected")
                quit()
            elif message.startswith("Player"):
                self.player_number = int(message.split()[1])
                print(f"You are Player {self.player_number}")

    def draw_card_with_animation(self, card_image, start_pos, end_pos, progress):
        """Draw a card with animation"""
        if progress >= 1.0:
            self.screen.blit(card_image, end_pos)
            return

        # Calculate current position
        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        
        # Draw card at current position
        self.screen.blit(card_image, (current_x, current_y))

    async def draw_game_state(self):
        self.screen.fill((255, 255, 255))
        
        # Calculate positions based on window size
        padding = int(self.window_width * 0.05)  # 5% padding
        card_spacing = int(self.window_width * 0.15)  # 15% spacing between cards (reduced from 20%)
        
        # Draw player information
        player_text = f"Player {self.player_number}"
        turn_text = f"Current Turn: Player {self.current_player}"
        self.screen.blit(self.font.render(player_text, True, (0, 0, 0)), (padding, padding))
        self.screen.blit(self.font.render(turn_text, True, (0, 0, 0)), (padding, padding * 2))

        # Draw cards for both players
        current_time = pygame.time.get_ticks()
        animation_progress = min(1.0, (current_time - self.last_draw_time) / self.draw_animation_duration)
        
        print(f"Drawing cards: {self.drawn_cards}")
        for player, card in self.drawn_cards.items():
            if card and "art" in card:
                try:
                    image_path = self.images_path / card["art"]
                    print(f"Attempting to load image from: {image_path}")
                    print(f"Image path exists: {image_path.exists()}")
                    print(f"Image path is file: {image_path.is_file()}")
                    
                    if not image_path.exists():
                        print(f"ERROR: Image file not found at {image_path}")
                        continue
                        
                    card_image = pygame.image.load(str(image_path))
                    print(f"Successfully loaded image: {card_image.get_size()}")
                    
                    card_image = pygame.transform.scale(card_image, (self.card_width, self.card_height))
                    print(f"Scaled image size: {card_image.get_size()}")
                    
                    # Calculate positions
                    x_pos = padding + (player - 1) * card_spacing
                    y_pos = int(self.window_height * 0.3) if player == 1 else int(self.window_height * 0.6)
                    
                    print(f"Drawing card at position: ({x_pos}, {y_pos})")
                    # Draw card with animation
                    start_pos = (self.window_width // 2, self.window_height // 2)  # Start from center
                    end_pos = (x_pos, y_pos)
                    self.draw_card_with_animation(card_image, start_pos, end_pos, animation_progress)
                    
                    # Draw player label under the card
                    player_label = self.font.render(f"Player {player}", True, (0, 0, 0))
                    label_pos = (x_pos + self.card_width // 2 - player_label.get_width() // 2,
                               y_pos + self.card_height + 10)
                    self.screen.blit(player_label, label_pos)
                    
                except Exception as e:
                    print(f"Error loading card image: {e}")
                    # Draw a placeholder rectangle if image loading fails
                    rect = pygame.Rect(x_pos, y_pos, self.card_width, self.card_height)
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)
                    error_text = self.font.render("Card", True, (0, 0, 0))
                    text_rect = error_text.get_rect(center=rect.center)
                    self.screen.blit(error_text, text_rect)

        pygame.display.flip()

    async def handle_input(self, writer):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(f"Player {self.player_number} requesting card draw")
                    writer.write("draw_card".encode())
                    await writer.drain()

    async def receive(self, reader):
        while self.running:
            try:
                data = await reader.read(1024)
                if data:
                    message = data.decode()
                    await self.handle_server_message(message)
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    async def main(self):
        try:
            print(f"Connecting to server at {self.host}:{self.port}")
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print("Connected to server")
            
            # Start receiving messages
            receive_task = asyncio.create_task(self.receive(reader))
            
            while self.running:
                await self.handle_input(writer)
                await self.draw_game_state()
                await asyncio.sleep(0.016)  # ~60 FPS

            receive_task.cancel()
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            pygame.quit()

async def main():
    client = GameClient("10.5.1.252", 3945)
    await client.main()

if __name__ == "__main__":
    asyncio.run(main())

