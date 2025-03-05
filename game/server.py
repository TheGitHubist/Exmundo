import asyncio
import pygame

# Initialize Pygame
pygame.init()

# Server settings
HOST = '127.0.0.1'
PORT = 8888

connected_clients = []  # List to keep track of connected clients

async def handle_client(reader, writer):
    connected_clients.append(writer)  # Add new client to the list

    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    print("Sending response back to the client.")
    writer.write(data)
    await writer.drain()

    # Notify all clients that a new user has connected
    message = "Someone is connected"
    for client in connected_clients:
        client.write(message.encode())
        await client.drain()

    print("Closing the connection.")

    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

# Run the server
if __name__ == '__main__':
    asyncio.run(main())
