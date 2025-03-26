import asyncio
import pygame
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from game.deck import PlayerDeck
from game.game_manager import GameManager

port = 3945
pygame.init()

class GameServer:
    def __init__(self):
        self.game_manager = GameManager()
        self.connected_players = []
        self.game_started = False
        self.images_path = Path(__file__).parent.parent / 'images'
        print(f"Server images path: {self.images_path}")
        print(f"Images path exists: {self.images_path.exists()}")
        
        # Load available card images
        self.available_cards = [f.name for f in self.images_path.glob('*.png')]
        print(f"Available cards: {self.available_cards}")
        if not self.available_cards:
            print("WARNING: No card images found!")
        else:
            for card in self.available_cards:
                card_path = self.images_path / card
                print(f"Card {card} exists: {card_path.exists()}")
                print(f"Card {card} is file: {card_path.is_file()}")

    async def handle_client_msg(self, reader, writer):
        addr = writer.get_extra_info('peername')
        player_number = len(self.connected_players) + 1
        
        if player_number > 2:
            writer.write("Game is full".encode())
            await writer.drain()
            return

        self.connected_players.append((addr, writer))
        writer.write(f"Player {player_number}".encode())
        await writer.drain()
        print(f"Player {player_number} connected from {addr}")

        if len(self.connected_players) == 2:
            self.game_started = True
            print("Game started with 2 players!")
            # Notify both players that game has started
            for _, writer in self.connected_players:
                writer.write("Game started".encode())
                await writer.drain()

        while True:
            try:
                data = await reader.read(1024)
                if data == b'':
                    break

                message = data.decode()
                print(f"Received message from player {player_number}: {message}")
                
                if message == "draw_card":
                    if self.game_manager.is_player_turn(player_number):
                        # For testing, use available card images
                        if self.available_cards:
                            card_index = player_number % len(self.available_cards)
                            card_name = self.available_cards[card_index]
                            card = {
                                "art": card_name
                            }
                            print(f"Drawing card for player {player_number}: {card}")
                            print(f"Using card index {card_index}: {card_name}")
                            
                            # Notify both players about the card draw
                            response = json.dumps({
                                "type": "card_drawn",
                                "player": player_number,
                                "card": card
                            })
                            print(f"Sending card data: {response}")
                            for _, writer in self.connected_players:
                                writer.write(response.encode())
                                await writer.drain()
                                print("Card data sent to player")
                        else:
                            print("No cards available to draw!")
                        
                        self.game_manager.switch_player()
                        # Notify both players about turn change
                        turn_msg = json.dumps({
                            "type": "turn_change",
                            "current_player": self.game_manager.get_current_player()
                        })
                        for _, writer in self.connected_players:
                            writer.write(turn_msg.encode())
                            await writer.drain()

            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break

        self.connected_players.remove((addr, writer))
        writer.close()
        await writer.wait_closed()
        print(f"Player {player_number} disconnected")
        writer.close()

async def main():
    game_server = GameServer()
    server = await asyncio.start_server(game_server.handle_client_msg, '', port)
    
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Server running on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
