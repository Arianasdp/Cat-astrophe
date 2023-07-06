from support import import_folder
import pygame 

class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,x_shift): #actualiza la posición horizontal de los cuadrados
		self.rect.x += x_shift
		
    # Al ajustar la posición del sprite en relación con el desplazamiento de la cámara, 
    # se crea la ilusión de que el sprite se está moviendo en la pantalla mientras el punto de vista cambia
    # O sea que el sprite se mueve en relación con el cambio de posición de la cámara, 
    # lo que da la impresión de movimiento mientras el punto de vista se desplaza.

class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface
		
class AnimatedTile(Tile):
	def __init__(self,size,x,y,path,speed):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.frame_speed = speed
		self.image = self.frames[self.frame_index]
		
	def animate(self):
		self.frame_index += self.frame_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
	def update(self, x_shift):
		self.animate()
		self.rect.x += x_shift

class Life(AnimatedTile):
	def __init__(self,size,x,y,path,speed):
		super().__init__(size,x,y,path,speed)
		center_x = x + 38 #int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))

class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,speed,offset):
		super().__init__(size,x,y,path,speed)
		offset_y = y - offset
		self.rect.topleft = (x,offset_y)


		
		