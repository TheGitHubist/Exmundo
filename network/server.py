import asyncio
import pygame
import json
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from game.debug import debug, read_message

port = 3945
pygame.init()

class GameServer:
    def __init__(self):
        self.connected_players = {}  # Map writer to self.player_number

    async def read_client(self, reader, writer):
        data = await reader.read(1024)
        if data == b'':
            return False   
          
        message = data.decode()

        self.player_number = self.connected_players.get(writer, None)
        if self.player_number is None:
            debug(f"Received message from unknown player {self.addr}",True)
            return False  

        debug(f"Received message from player {self.player_number}: {message[0]}",True)
        return message

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

        # Notify remaining players about disconnection
        for remaining_writer in self.connected_players.keys():
            try:
                remaining_writer.write(read_message(1,'client down').encode())
                await remaining_writer.drain()
            except Exception as e:
                debug(f"Error notifying remaining player: {e}",True)

    async def full_connection(self,reader,writer):
        writer.write(read_message(1,'full client').encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
    
    async def handle_client_msg(self, reader, writer):
        self.addr = writer.get_extra_info('peername')

        # Assign player number
        if len(self.connected_players) >= 2:
            self.full_connection(reader,writer)

        # Assign next available player number (1 or 2)
        assigned_numbers = set(self.connected_players.values())
        if 1 not in assigned_numbers:
            self.player_number = 1
        elif 2 not in assigned_numbers:
            self.player_number = 2
        else:
            # Should not happen due to earlier check
            self.full_connection(reader,writer)

        self.connected_players[writer] = self.player_number
        writer.write(f"{read_message(1,'assign number player')}[]{self.player_number}".encode())
        await writer.drain()
        debug(f"Player {self.player_number} connected from {self.addr}",False)

        if len(self.connected_players) == 2:
            debug("Game started with 2 players!",False)
            # Notify both players that game has started
            for player_writer in self.connected_players.keys():
                player_writer.write(read_message(1,'start game').encode())
                await player_writer.drain()

        while True:
            try:
                message = await self.read_client(reader, writer)
                if message == False:
                    break

                message = message.split("[]")
                if message[0] == "202":
                    writer.write(read_message(1,'Update ?').encode())
                elif message[0] == "203":
                    debug(f"Player {self.player_number} Is Dumb")
                elif message[0] == "204":
                    debug("Download =}")
                elif message[0] == 205:
                    debug(f"Player {self.player_number} as {message[1]}")
                elif message[0] == "206":
                    debug(f"Player {self.player_number} as {message[1]}")
                elif message[0] == "210":
                    debug(f"Player {self.player_number} as {message[1]}")
                elif message[0] == "211":
                    debug(f"Player {self.player_number} as {message[1]}")
                await writer.drain()
            except Exception as e:
                debug(f"Error handling client {self.addr}: {e}",True)
                break

        await self.disconnect(reader, writer)

async def main():
    game_server = GameServer()
    server = await asyncio.start_server(game_server.handle_client_msg, '', port)
    
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    debug(f'Server running on {addrs}',True)

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
