import pygame
from settings import *
from pygame.math import Vector2 as vector
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, colliders):
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = "right_idle" 
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.pos =  vector(self.rect.center)
        self.direction = vector()
        self.speed = 400
        
        
        # collision
        self.old_rect =  self.rect.copy()
        self.collision_sprites =  colliders
        
        
    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else: 
                for name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    loc_path = folder[0].replace("\\","/") + "/" + name
                    surf = pygame.image.load(loc_path).convert_alpha()
                    key = folder[0].split('\\')[2]
                    self.animations[key].append(surf)
    
    def animate(self, dt):
        self.frame_index += 7*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # horizontal input
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        else: 
            self.direction.x = 0
            
        # vertical input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            # self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            # self.status = "dow"
        else:
            self.direction.y = 0
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                
                if direction == "horizontal":
                    # left collision
                    if self.rect.left <= sprite.rect.right\
                    and self.old_rect.left >= sprite.old_rect.right:
                        
                        self.rect.left = sprite.rect.right
                    # right collision
                    elif self.rect.right >= sprite.rect.left\
                    and self.old_rect.right <= sprite.old_rect.left:
                        
                        self.rect.right = sprite.rect.left 
                    self.pos.x = self.rect.x
                else:
                    if self.rect.bottom >= sprite.rect.top\
                    and self.old_rect.bottom <= sprite.old_rect.top:

                        self.rect.bottom = sprite.rect.top
                    elif self.rect.top <= sprite.rect.bottom\
                        and self.old_rect.top >= sprite.old_rect.bottom:
                        
                        self.rect.top =  sprite.rect.bottom
                    self.pos.y = self.rect.y
            
    def move(self, dt):
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision("horizontal")
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collision("vertical")
        
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.animate(dt)