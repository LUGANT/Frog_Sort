from modules.game_module import GameHandler
import pygame

gameHandler = GameHandler()
pygame.init()

gameHandler.load_background()
gameHandler.flip()

# Game Loop
running = True
while running:
    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False