import pygame as pg
import asyncio
from pathlib import Path
from mecanics import Turn
from deck import PlayerDeck as Player

def main():
    connection_status = ""
    drawn_card_image = None

    pg.init()
    screen = pg.display.set_mode((1500, 900))
    running = True
    asyncio.set_event_loop(asyncio.new_event_loop())

    player = Player()
    turn = Turn(player)

    while running:
        for event in pg.event.get(): 
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                connection_status = "You are connected"
                #asyncio.create_task(send_message("Hello, Server!"))
                drawn_card = turn.drawPhase()
                if drawn_card:
                    drawn_card_image = pg.image.load(f'images/{drawn_card["art"]}')

            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))        
        # Display connection status message
        font = pg.font.Font(None, 74)
        text = font.render(connection_status, True, (0, 0, 0))
        screen.blit(text, (50, 50))  # Display text at position (50, 50)

        # Display drawn card image
        if drawn_card_image:
            screen.blit(drawn_card_image, (100, 100))

        pg.display.flip()        
        # Reset connection status after displaying
        connection_status = ""

    pg.quit()

if __name__ == "__main__":
    main()
