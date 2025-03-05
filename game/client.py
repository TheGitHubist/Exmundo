import asyncio
import pygame

# Initialize Pygame
pygame.init()

# Server settings
HOST = '127.0.0.1'
PORT = 8888

async def send_message(message):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    print(f'Sending: {message}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    print("Closing the connection.")
    writer.close()

async def handle_incoming_messages():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    while True:
        data = await reader.read(100)
        if data:
            message = data.decode()
            print(message)  # Display the message in the console
        else:
            break

async def main():
    # Start listening for incoming messages
    asyncio.create_task(handle_incoming_messages())
    message = "Hello, Server!"
    await send_message(message)


# Run the client
if __name__ == '__main__':
    asyncio.run(main())
