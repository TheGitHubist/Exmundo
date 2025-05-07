import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import time
import json
from pathlib import Path
import re

from game.deck import PlayerDeck as Player
from game.debug import debug, read_message
from game.game_manager import GameManager
from game.screen import Screen

class GameClient(Screen):
    def __init__(self, host, port):
        super().__init__()
        self.version = "0.0.1"
        self.game_manager = GameManager()
        self.choice()
        self.host = host
        self.port = port
        self.drawn_cards = {}  # Store drawn cards for both players
        self.last_draw_time = 0  # For animation
        self.draw_animation_duration = 500  # milliseconds
        self.game_started = False  # Track if game has started
        self.window_screen()

        self.images_path = Path(__file__).parent.parent / 'images'
        debug(f"Client images path: {self.images_path}\nImages path exists: {self.images_path.exists()}\nImages path absolute: {self.images_path.absolute()}",False)
        
        # Check if images directory exists and has files
        if not self.images_path.exists():
            debug(f"ERROR: Images directory not found at {self.images_path}",True)
        else:
            available_images = list(self.images_path.glob('*.png'))
            debug(f"Available images in directory: {[f.name for f in available_images]}",False)
            for img in available_images:
                debug(f"Image {img.name} exists: {img.exists()}\nImage {img.name} is file: {img.is_file()}\nImage {img.name} full path: {img.absolute()}",False)

    """Pour plus tard"""
    def choice(self):
        self.deck_choice = 0

    async def init_send(self, writer):
        writer.write(f"{read_message(0,'deck_choice')}[]{self.deck_choice}".encode())
        await writer.drain()

    def handle_resize(self, event):
        """Handle window resize events"""
        self.window_width = event.w
        self.window_height = event.h
        self.card_resize()

    async def Reader_server_message(self, message, writer):
        debug(f"Received message: {message}",True)
        message = message.split("[]")
        if message[0] == "101":
            debug("Client is down")
            self.stop()
        elif message[0] == "102":
            pass
        elif message[0] == "103":
            debug("Game is Full")
        elif message[0] == "104":
            debug("Card Npt Found")
        elif message[0] == "105":
            try:
                # Extract leading digits from the second word after "Player"
                player_str = message[1]
                match = re.match(r"(\d+)", player_str)
                if match:
                    self.player_number = int(match.group(1))
                    debug(f"You are Player {self.player_number}",True)
                else:
                    raise ValueError(f"No valid player number found in '{player_str}'")
            except ValueError as e:
                debug(f"Error parsing player number: {e}",True)
                self.stop()
        elif message[0] == "106":
            self.handle_input(self, writer)
        elif message[0] == "110":
            if message[1] == self.version:
                writer.write(read_message(0,'Update Yes').encode())
            else:
                writer.write(read_message(0,'Update No').encode())
        await writer.drain()


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


    async def draw_cards(self, writer):
        """Draw 5 cards for each player at game start"""
            
        debug(f"Starting initial card draw for player {self.player_number}",False)
        # Draw 5 cards for the current player
        for i in range(5):
            debug(f"Drawing initial card {i+1}/5 for player {self.player_number}",False)
            card = self.game_manager.player_deck.draw_to_hand()
            writer.write(f"{read_message(0,'My card')}[]{card}".encode())
            await writer.drain()
            # Wait longer between draws to ensure server processes each request
            await asyncio.sleep(0.5)
        debug(f"Initial card draw complete for player {self.player_number}",False)

    async def receive(self, reader, writer):
        while self.running:
            try:
                data = await reader.read(1024)
                if data:
                    message = data.decode()
                    await self.Reader_server_message(message, writer)
            except Exception as e:
                debug(f"Error receiving data: {e}",True)
                break

    async def main(self):
        try:
            debug(f"Connecting to server at {self.host}:{self.port}",True)
            reader, writer = await asyncio.open_connection(self.host, self.port)
            debug("Connected to server",False)
            
            # Start receiving messages
            receive_task = asyncio.create_task(self.receive(reader, writer))
            
            # Wait a bit to ensure initial messages are received
            await asyncio.sleep(0.5)
            
            await self.init_send(writer)
            
            while self.running:
                await self.handle_input(writer)
                await asyncio.sleep(0.016)  # ~60 FPS

            receive_task.cancel()
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            debug(f"Connection error: {e}",False)
        finally:
            self.stop()


async def main():
    client = GameClient("10.5.1.100", 3945)
    await client.main()

if __name__ == "__main__":
    asyncio.run(main())