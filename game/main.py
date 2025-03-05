import pygame as pg
import asyncio
from game.client import send_message

from pathlib import Path

def main():
    connection_status = ""  # Variable to hold connection status messages

    pg.init()
    screen = pg.display.set_mode((1500, 900))
    running = True
    asyncio.set_event_loop(asyncio.new_event_loop())  # Set up a new event loop for asyncio

    while running:
        for event in pg.event.get(): 
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:  # Check for spacebar press
                connection_status = "You are connected"  # Update connection status
                asyncio.create_task(send_message("Hello, Server!"))  # Send message to server

            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))        
        # Display connection status message
        font = pg.font.Font(None, 74)
        text = font.render(connection_status, True, (0, 0, 0))
        screen.blit(text, (50, 50))  # Display text at position (50, 50)

        pg.display.flip()        
        # Reset connection status after displaying
        connection_status = ""

    pg.quit()

if __name__ == "__main__":
    main()
