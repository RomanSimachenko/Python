import pygame,sys,random
pygame.init()
clock=pygame.time.Clock()
display_info=pygame.display.Info()
width,height=display_info.current_w//2,display_info.current_h//2
def colors():
	global WHITE,BLACK,RED,GREEN,BLUE
	WHITE=(255, 255, 255)
	BLACK=(0, 0, 0)
	RED=(255, 0, 0)
	GREEN=(0, 255, 0)
	BLUE=(0, 0, 255)
colors()
FPS=60
display=pygame.display.set_mode((width,height))
pygame.display.set_caption("Testing")
run=True
while run:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
			pygame.quit()
			quit()
			sys.exit()
	display.fill(BLACK)
	pygame.display.update()