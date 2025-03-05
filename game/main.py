import pygame as pg
import socket

from pathlib import Path


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started, waiting for connections...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        client_socket.close()

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server!")
    client_socket.close()

def main():
    pg.init()
    screen = pg.display.set_mode((1500, 900))
    running = True
    server_thread = None


    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pg.display.flip()
    pg.quit()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started, waiting for connections...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        client_socket.close()


def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    print("Connected to the server!")
    client_socket.close()


if __name__ == "__main__":

    main()
