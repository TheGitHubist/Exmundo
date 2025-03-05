import asyncio
import pygame

# Initialize Pygame
pygame.init()

# Server settings
HOST = '127.0.0.1'
PORT = 8888

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    print("Sending response back to the client.")
    writer.write(data)
    await writer.drain()

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
