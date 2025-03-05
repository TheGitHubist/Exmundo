import asyncio
import pygame

pygame.init()

class client:
    def __init__(self, message):
        self.port = 3945
        self.host = "10.5.1.44"
        self.message = message

    async def inputs(self, writer):
        while True:
            if self.message != "":
                writer.write(massage.encode())
                message = ""
                await writer.drain()

    async def receive(self, reader):
        while True:
            data = await reader.read(1024)
            print(data.decode())

    async def main():
        reader, writer = await asyncio.open_connection(self.host, self.port)
        if(await asyncio.gather(self.inputs(writer),self.receive(reader)) == 1):
            exit(1)

if __name__ == "__main__":
    c = client("Salut")
    asyncio.run(c.main())
