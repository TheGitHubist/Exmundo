import asyncio
import pygame
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from game.deck import PlayerDeck
from game.game_manager import GameManager
from game.debug import debug

port = 3945
pygame.init()

class GameServer:
    def __init__(self):
        self.game_manager = GameManager()
        self.connected_players = {}  # Map writer to self.player_number
        self.images_path = Path(__file__).parent.parent / 'images'
        debug(f"Server images path: {self.images_path}",False)
        debug(f"Images path exists: {self.images_path.exists()}",False)

        """ Load available card images """
        self.available_cards = [f.name for f in self.images_path.glob('*.png')]
        debug(f"Available cards: {self.available_cards}",False)
        if not self.available_cards:
            debug("WARNING: No card images found!",False)
        else:
            for card in self.available_cards:
                card_path = self.images_path / card
                debug(f"Card {card} exists: {card_path.exists()}",False)
                debug(f"Card {card} is file: {card_path.is_file()}",False)
                debug(f"Card {card} full path: {card_path.absolute()}",False)

                # Test load each image
                try:
                    test_image = pygame.image.load(str(card_path))
                    debug(f"Successfully loaded test image for {card}: {test_image.get_size()}",False)
                except Exception as e:
                    debug(f"Error loading test image for {card}: {e}",False)
                    pass

    async def getdeck(self, message):
        parts = message.split()
        if len(parts) > 1 and parts[0] == "569":
                    if self.player_number == 1:
                        self.game_manager.player1_deck.choice_deck(int(parts[1]))
                    elif self.player_number == 2:
                        self.game_manager.player2_deck.choice_deck(int(parts[1]))

    async def read_client(self, reader, writer):
        data = await reader.read(1024)
        if data == b'':
            return False   
          
        message = data.decode()

        self.player_number = self.connected_players.get(writer, None)
        if self.player_number is None:
            debug(f"Received message from unknown player {self.addr}",True)
            return False  

        debug(f"Received message from player {self.player_number}: {message}",True)
        return message

    async def draw_card(self, message , reader, writer):
        if message == "draw_card":
            if self.game_manager.is_player_turn(self.player_number):
                card = self.game_manager.draw_card(self.player_number)
                if card:
                    response = json.dumps({
                        "type": "card_drawn",
                        "player": self.player_number,
                        "card": card.to_dict() if hasattr(card, "to_dict") else str(card)
                    })
                    debug(f"Sending card data: {response}",True)

                    # Send to all players and wait for each to complete
                    for player_writer in self.connected_players.keys():
                        player_writer.write(response.encode())
                        await player_writer.drain()
                        debug(f"Card data sent to player",True)

                    # Wait a small delay to ensure messages are sent
                    await asyncio.sleep(0.1)

                    # Send turn change message
                    turn_msg = json.dumps({
                        "type": "turn_change",
                        "current_player": self.game_manager.get_current_player()
                    })
                    for player_writer in self.connected_players.keys():
                        player_writer.write(turn_msg.encode())
                        await player_writer.drain()
                        debug(f"Turn change sent to player",True)

                    self.game_manager.switch_player()
                else:
                    debug("No cards available to draw!",True)
            else:
                debug(f"Not player's turn! : {self.game_manager.current_player}, {self.player_number}",True)

    async def disconnect(self, reader, writer):
        # Handle player disconnection and log the event
        if writer in self.connected_players:
            self.player_number = self.connected_players[writer]
            del self.connected_players[writer]
        else:
            debug(f"Warning: Tried to remove player {self.addr} but not found in connected_players.",True)
        writer.close()
        await writer.wait_closed()
        debug(f"Player {self.player_number} disconnected",True)

        # Reset game state if a player disconnects
        self.game_manager.game_started = False
        self.game_manager = GameManager()  # Reset game manager

        # Notify remaining players about disconnection
        for remaining_writer in self.connected_players.keys():
            try:
                remaining_writer.write("Player disconnected".encode())
                await remaining_writer.drain()
            except Exception as e:
                debug(f"Error notifying remaining player: {e}",True)

    async def handle_client_msg(self, reader, writer):
        self.addr = writer.get_extra_info('peername')

        # Assign player number
        if len(self.connected_players) >= 2:
            writer.write("Game is full".encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        # Assign next available player number (1 or 2)
        assigned_numbers = set(self.connected_players.values())
        if 1 not in assigned_numbers:
            self.player_number = 1
        elif 2 not in assigned_numbers:
            self.player_number = 2
        else:
            # Should not happen due to earlier check
            writer.write("Game is full".encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        self.connected_players[writer] = self.player_number
        writer.write(f"Player {self.player_number}".encode())
        await writer.drain()
        debug(f"Player {self.player_number} connected from {self.addr}",False)

        if len(self.connected_players) == 2:
            self.game_manager.game_started = True
            debug("Game started with 2 players!",False)
            # Notify both players that game has started
            for player_writer in self.connected_players.keys():
                player_writer.write("Game started".encode())
                await player_writer.drain()

        while True:
            try:
                message = await self.read_client(reader, writer)
                if message == False:
                    break
                await self.getdeck(message)
                await self.draw_card(message, reader, writer)


            except Exception as e:
                debug(f"Error handling client {self.addr}: {e}",True)
                break

        await self.disconnect(reader, writer)

async def main():
    debug("Testing",True)
    game_server = GameServer()
    server = await asyncio.start_server(game_server.handle_client_msg, '', port)
    
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    debug(f'Server running on {addrs}',True)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
