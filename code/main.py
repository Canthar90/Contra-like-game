import pygame, sys
from settings import * 
from pytmx.util_pygame import load_pygame
from tile import Tile, CollisionTile, MovingPlatform
from player import Player
from pygame.math import Vector2 as vector
from bullet import Bullet, FireAnimation
from enemy import Enemy


class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()
		
		# import
		self.fg_sky = pygame.image.load(r"graphics\sky\fg_sky.png").convert_alpha()
		self.bg_sky =  pygame.image.load(r"graphics\sky\bg_sky.png").convert_alpha()
		tmx_map = load_pygame("C:\projects\Contra-like-game\data\map.tmx")
		
		# dimentions
		self.padding =  WINDOW_WIDTH / 2
		self.sky_width = self.bg_sky.get_width()
		map_width =  tmx_map.tilewidth * tmx_map.width + (2 * self.padding)
		self.sky_num = int(map_width // self.sky_width)
        
        
	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

		for x in range(self.sky_num):
			x_pos = -self.padding + (x * self.sky_width)
			self.display_surface.blit(self.bg_sky, (x_pos - self.offset.x/2.5, 800 - self.offset.y/2.5))
			self.display_surface.blit(self.fg_sky, (x_pos - self.offset.x/2, 800 - self.offset.y/2))

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
		self.platform_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.setup()
  
		# bullet images
		self.bullet_surf = pygame.image.load(r"graphics\bullet.png").convert_alpha()
		self.fire_surfs = [pygame.image.load(r"graphics\fire\0.png").convert_alpha(),
                     pygame.image.load(r"graphics\fire\1.png").convert_alpha()]
  
	def shoot(self, pos, direction, entity):
		Bullet(pos, self.bullet_surf ,direction, [self.all_sprites, self.bullet_sprites])
		FireAnimation(entity, self.fire_surfs, direction, self.all_sprites)
  
	def bullet_collisions(self):
		# obstacle 
		for obstacle in self.colission_sprites.sprites():
			pygame.sprite.spritecollide(obstacle, self.bullet_sprites, True)
  
		# entities
  
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
                         path=r"graphics\player", colliders=self.colission_sprites,
                         shoot=self.shoot)
			if obj.name == "Enemy":
				Enemy(pos=(obj.x, obj.y), path=r"graphics\enemies",
          			groups=self.all_sprites, shoot=self.shoot,
          			player=self.player, collison_sprites=self.colission_sprites)

		# details for the foreground objects
		for x, y, surf in tmx_map.get_layer_by_name("FG Detail Bottom").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="FG Detail Bottom")

		# foreground top details
		for x, y, surf in tmx_map.get_layer_by_name("FG Detail Top").tiles():
			Tile(pos=(x*64, y*64), surf=surf, groups=self.all_sprites, z="FG Detail Top")

		self.platform_border_rects = []
		for obj in tmx_map.get_layer_by_name("Platforms"):
			if obj.name == "Platform":
				MovingPlatform(pos=(obj.x, obj.y),
                   surf=obj.image, 
                   groups=[self.all_sprites, 
                           self.colission_sprites, self.platform_sprites])
			else: # border
				border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
				self.platform_border_rects.append(border_rect)
		
	def platform_collisions(self):
		for platform in self.platform_sprites.sprites():
			for border in self.platform_border_rects:
				# boune the platforms 
				if platform.rect.colliderect(border):
					if platform.direction.y < 0:
						platform.rect.top = border.bottom
						platform.pos.y = platform.rect.y
						platform.direction.y = 1
					else:
						platform.rect.bottom = border.top
						platform.pos.y = platform.rect.y
						platform.direction.y = -1
      
			if platform.rect.colliderect(self.player.rect) and \
   				self.player.rect.centery > platform.rect.centery:

				platform.pos.y = platform.rect.y
				platform.direction.y = -1
       
					

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
		
			dt = self.clock.tick() / 1000
			self.display_surface.fill((249,131,103))

			self.platform_collisions()
			self.all_sprites.update(dt)
			self.all_sprites.custom_draw(self.player)
			self.bullet_collisions()

			pygame.display.update()

if __name__ == '__main__':
	main = Main()
	main.run()
