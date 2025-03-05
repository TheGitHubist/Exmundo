import asyncio
import pygame

port = 3945
host = "10.5.1.44"
pygame.init()

class client:
    async def run(self):
        self.reader, self.writer = await asyncio.open_connection(host, port)
        if(await asyncio.gather(inputs(writer),receive(reader)) == 1):
            exit(1)

    async def inputs(writer, message):
        writer.write(massage.encode())
        await writer.drain()

    async def receive(reader):
        while True:
            data = await reader.read(1024)
            print(data.decode())

if __name__ == "__main__":
    c = client()
    asyncio.run(c.run)
