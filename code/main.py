import pygame, sys
from settings import * 
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile
from player import Player
from pygame.math import Vector2 as vector



class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        
        # sprites inside the group
        for sprite in self.sprites():
            offset_rect =  sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
            

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Contra_like')
		self.clock = pygame.time.Clock()
		
		# groups
		self.all_sprites = AllSprites()
		self.colission_sprites = pygame.sprite.Group()
		self.setup()
  
	def setup(self):
		tmx_map = load_pygame("data\map.tmx")

		# backgroun objects
		for x, y, surf in tmx_map.get_layer_by_name("BG").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="BG")

		# detailed background objects
		for x, y, surf in tmx_map.get_layer_by_name("BG Detail").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="BG Detail")

		# collision object
		for x, y, surf in tmx_map.get_layer_by_name("Level").tiles():
			CollisionTile(pos=(x*64, y*64), surf=surf,
                 		groups=[self.all_sprites, self.colission_sprites])
		
		# objects 
		for obj in tmx_map.get_layer_by_name("Entities"):
			if obj.name == 'Player':
				self.player = Player(pos=(obj.x, obj.y), groups=self.all_sprites,
                         path=r"graphics\player")

		# details for the foreground objects
		for x, y, surf in tmx_map.get_layer_by_name("FG Detail Bottom").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="FG Detail Bottom")

		# foreground top details
		for x, y, surf in tmx_map.get_layer_by_name("FG Detail Top").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="FG Detail Top")
       
		

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
		
			dt = self.clock.tick() / 1000
			self.display_surface.fill((249,131,103))

			self.all_sprites.update(dt)
			self.all_sprites.custom_draw(self.player)

			pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()
