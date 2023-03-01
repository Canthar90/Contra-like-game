import pygame
from settings import *
from pygame.math import Vector2 as vector
from entity import Entity


class Enemy(Entity):
    def __init__(self, pos, path, groups, shoot, player, collison_sprites):
        super().__init__(pos, path, groups, shoot)
        self.player = player
    
        for sprite in collison_sprites.sprites():
            if sprite.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = sprite.rect.top
                    
        self.cooldown = 580
                
                
    def get_status(self):
        if self.player.rect.centerx <  self.rect.centerx:
            self.status = "left_idle"
        else:
            self.status = "right_idle"
    
    def check_fire(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        
        distance = (player_pos - enemy_pos).magnitude()
        same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False
        
        if distance < 600 and same_y and not self.is_shooting:
            bullet_direction = vector(1, 0) if self.status == "right_idle" else vector(-1, 0)
            y_offset = vector(0, -16)
            pos =  self.rect.center + bullet_direction * 60
            self.shoot(pos + y_offset, bullet_direction, self)
            
            self.is_shooting = True
            self.shoot_time = pygame.time.get_ticks()
            
    def update(self, dt):
        self.animate(dt)
        self.get_status()
        
        self.shoot_timer()
        self.check_fire()
        self.check_death()
        