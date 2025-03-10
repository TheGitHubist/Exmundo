import asyncio
import time
import pygame

pygame.init()

class client:
    def __init__(self, message):
        self.port = 3945
        self.host = "10.5.1.44"
        self.message = message

    # async def inputs(self, writer):
    #     while True:
    #         writer.write(self.message.encode())
    #         self.message = ""
    #         await writer.drain()

    # async def receive(self, reader):
    #     while True:
    #         data = await reader.read(1024)
    #         print(data.decode())

    # async def main(self):
    #     reader, writer = await asyncio.open_connection(self.host, self.port)
        
    #     writer.write(b"Salut")
    #     await writer.drain()

    #     message = 10

    #     while True:
    #         data = await reader.read(1024)

    #         if not data:
    #             raise Exception("socket closed")

    #         print(f"Received: {data.decode()!r}")

    #         if message > 0:
    #             await asyncio.sleep(1)
    #             writer.write(f"{self.message}".encode())
    #             self.message = ""
    #             await writer.drain()
    #             message -= 1
    #         else:
    #             writer.write(b"quit")
    #             await writer.drain()
    #             break

    async def inputs(self, writer):
        while True:
            writer.write(self.message.encode())
            self.message = ""
            await asyncio.sleep(0.1)
            await writer.drain()
            

    async def receive(self, reader):
        while True:
            data = await reader.read(1024)
            print(data.decode())

    async def main(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        if(await asyncio.gather(self.inputs(writer),self.receive(reader), main_game(self)) == 1): #Changer le main_game()
            exit(1)





async def main_game(client):
    client.message = "azerty"
        

if __name__ == "__main__":
    c = client("Salut")
    asyncio.run(c.main())

