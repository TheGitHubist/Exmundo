import asyncio
import pygame

# Initialize Pygame
pygame.init()

async def handle_client_msg(reader, writer):
    while True:

        addr = writer.get_extra_info('peername')
        data = await reader.read(1024)
        if data == b'':
            break

        message = data.decode()
        print(f"Message Received from {addr[0]}:{addr[1]} : {message!r}")

        writer.write(f"Hello client ! Received <{message!r}>".encode())
        await writer.drain()


async def main():

    server = await asyncio.start_server(handle_client_msg, '', 13337)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Run on Port:13337')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":

    asyncio.run(main())
