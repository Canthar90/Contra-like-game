import pygame
from settings import *
from pygame.math import Vector2 as vector
from os import walk
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups, shoot):
        super().__init__(groups)
        
        # assets setup
        self.import_assets(path)
        self.frame_index = 0
        self.status = "right_idle" 
        
        # image setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["main"]
        self.old_rect =  self.rect.copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.pos =  vector(self.rect.center)
        self.direction = vector()
        self.speed = 400
        
        # interaction
        self.shoot = shoot
        # create a bullet timer
        self.is_shooting = False
        self.shoot_time = None
        self.duck = False
        self.cooldown = 200
        
        # health
        self.health = 3
        
        self.is_vurnerable = True
        self.invulnerability_delta = 350
        self.hit_time = None
        self.damage_sound = pygame.mixer.Sound("audio\hit.wav")
        self.damage_sound.set_volume(0.4)
        
    def blink(self):
        if not self.is_vurnerable:
            if self.wawe_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf
    
    def wawe_value(self):
        value = sin(pygame.time.get_ticks())
        return True if value >=0 else False
    
    def damage(self):
        if self.is_vurnerable:
            self.health -= 1
            self.is_vurnerable = False
            self.hit_time = pygame.time.get_ticks()
            self.damage_sound.play()
        
    def check_death(self):
        if self.health <= 0:
            self.kill()
    
    def animate(self, dt):
        self.frame_index += 7*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
            
        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
    
    def shoot_timer(self):
        if self.is_shooting:    
            if pygame.time.get_ticks() - self.shoot_time > self.cooldown:
                self.is_shooting = False
    
    def invul_timer(self):
        if not self.is_vurnerable:
            delta_time = pygame.time.get_ticks()- self.hit_time    
            if delta_time > self.cooldown:
                self.is_vurnerable = True
        
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