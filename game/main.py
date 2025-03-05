import pygame as pg

from pathlib import Path

def main():
    pg.init()
    screen = pg.display.set_mode((1500, 900))
    running = True


    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pg.display.flip()
    pg.quit()


if __name__ == "__main__":

    main()
