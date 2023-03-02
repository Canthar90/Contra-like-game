import pygame


class Overlay:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.health_surf = pygame.image.load("graphics\health.png").convert_alpha()    
    
    def display(self):
        for r in range(self.player.health):
            self.display_surface.blit(self.health_surf, (5 + r*20, 10))