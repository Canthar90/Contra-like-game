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
        
        # vertical movement
        self.gravity = 15
        self.jump_speed = 1400
        self.on_floor = False
        self.duck = False
        self.moving_floor = None
        
    def get_status(self):
        # idle
        if self.direction.x == 0 and self.on_floor :
            self.status = self.status.split("_")[0] + "_idle"
        # jump
        if self.direction.y != 0 and not self.on_floor:
            self.status = self.status.split("_")[0] + "_jump"
        # duck
        if self.duck and self.direction.x == 0 and self.on_floor:
            self.status = self.status.split("_")[0] + "_duck"
        
    def check_contact(self):
        bottom_rect = pygame.Rect(0,0,self.rect.width,5)
        bottom_rect.midtop = self.rect.midbottom  
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(bottom_rect):
                if self.direction.y > 0:
                    self.on_floor = True  
                if hasattr(sprite, "direction"):
                    self.moving_floor = sprite        
        
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
            
        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = - self.jump_speed
            
        if keys[pygame.K_DOWN]:
            self.duck = True
        else:
            self.duck = False
    
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
                        self.on_floor = True
                        self.rect.bottom = sprite.rect.top
                    elif self.rect.top <= sprite.rect.bottom\
                        and self.old_rect.top >= sprite.old_rect.bottom:
                        
                        self.rect.top =  sprite.rect.bottom
                    self.pos.y = self.rect.y
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False
            
    def move(self, dt):
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collision("horizontal")
        
        # vertical movement
        # gravity
        
        self.direction.y += self.gravity
        self.pos.y += self.direction.y * dt
        self.moving_floor = None
        
        # glue the player to the platform
        if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:
            self.direction.y = 0
            self.rect.bottom = self.moving_floor.rect.top
            self.pos.y = self.rect.y
            self.on_floor = True
                    
        self.rect.y = round(self.pos.y)
        self.collision("vertical")
        
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.get_status()
        self.move(dt)
        self.check_contact()
        self.animate(dt)