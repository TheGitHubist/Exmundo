import asyncio
import pygame

port = 3945
host = "10.5.1.44"
message = ""
pygame.init()

async def inputs(writer):
    while True:
        writer.write(massage.encode())
        message = ""
        await writer.drain()

async def receive(reader):
    while True:
        data = await reader.read(1024)
        print(data.decode())

async def main():
    reader, writer = await asyncio.open_connection(host, port)
    if(await asyncio.gather(inputs(writer),receive(reader)) == 1):
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
