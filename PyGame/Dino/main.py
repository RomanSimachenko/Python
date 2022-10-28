import pygame
import random
pygame.init()

display_width=800
display_height=600
display=pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run Dino! Run!')
icon=pygame.image.load('icon.png')
pygame.display.set_icon(icon)
cactus_image=[pygame.image.load('Cactus0.png'),pygame.image.load('Cactus1.png'),pygame.image.load('Cactus2.png')]
cactus_options=[69,449,37,410,40,420]
stone_img=[pygame.image.load('Stone0.png'),pygame.image.load('Stone1.png')]
cloud_img=[pygame.image.load('Cloud0.png'),pygame.image.load('Cloud1.png')]
dino_img=[pygame.image.load('Dino0.png'),pygame.image.load('Dino1.png'),pygame.image.load('Dino2.png'),pygame.image.load('Dino3.png'),pygame.image.load('Dino4.png')]
img_counter=0
class Object:
	def __init__(self,x,y,width,image,speed):
		self.x=x
		self.y=y
		self.width=width
		self.image=image
		self.speed=speed
	def move(self):
		if self.x>=-self.width:
			display.blit(self.image,(self.x, self.y))
			self.x-=self.speed
			return True
		else:
			self.x=display_width+100+random.randrange(-80, 60)
			return False
	def return_self(self,radius,y,width,image):
		self.x=radius
		self.y=y
		self.width=width
		self.image=image
		display.blit(self.image,(self.x, self.y))
user_width=60
user_height=100
user_x=display_width//3
user_y=display_height-user_height-100
clock=pygame.time.Clock()
make_jump=False
jump_count=30
cactus_width=20
cactus_height=70
cactus_x=display_width-50
cactus_y=display_height-cactus_height-100
def jump():
	global user_y,make_jump,jump_count
	if jump_count>=-30:
		user_y-=jump_count/2.5
		jump_count-=1
	else:
		jump_count=30
		make_jump=False

def run_game():
	global make_jump
	game=True
	cactus_arr=[]
	create_cactus_arr(cactus_arr)
	Background=pygame.image.load('Background.png')
	stone,cloud=open_random_objects()
	while game:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			make_jump=True
		if keys[pygame.K_ESCAPE]:
			pause()
		if make_jump:
			jump()
		display.blit(Background,(0,0))
		draw_array(cactus_arr)
		move_objects(stone,cloud)
		draw_dino()
		if check_collision(cactus_arr):
			game=False
		pygame.display.update()
		clock.tick(60)
	return game_over()
def create_cactus_arr(array):
	choice=random.randrange(0,3)
	image=cactus_image[choice]
	width=cactus_options[choice*2]
	height=cactus_options[choice*2+1]
	array.append(Object(display_width+20,height,width,image,4))
	choice=random.randrange(0,3)
	image=cactus_image[choice]
	width=cactus_options[choice*2]
	height=cactus_options[choice*2+1]
	array.append(Object(display_width+20,height,width,image,4))
	choice=random.randrange(0,3)
	image=cactus_image[choice]
	width=cactus_options[choice*2]
	height=cactus_options[choice*2+1]
	array.append(Object(display_width+20,height,width,image,4))
def find_radius(array):
	maximum=max(array[0].x,array[1].x,array[2].x)
	if maximum<display_width:
		radius=display_width
		if radius-maximum<50:
			radius+=150
	else:
		radius=maximum
	choice=random.randrange(0,5)
	if choice==0:
		radius+=random.randrange(10,15)
	else:
		radius+=random.randrange(200,350)
	return radius
def draw_array(array):
	for cactus in array:
		check=cactus.move()
		if not check:
			radius=find_radius(array)
			choice=random.randrange(0,3)
			image=cactus_image[choice]
			width=cactus_options[choice*2]
			height=cactus_options[choice*2+1]
			cactus.return_self(radius,height,width,image)
def open_random_objects():
	choice=random.randrange(0,2)
	img_of_stone=stone_img[choice]
	choice=random.randrange(0,2)
	img_of_cloud=cloud_img[choice]
	stone=Object(display_width,display_height-80,10,img_of_stone,4)
	cloud=Object(display_width,80,70,img_of_cloud,2)
	return stone,cloud
def move_objects(stone,cloud):
	check=stone.move()
	if not check:
		choice=random.randrange(0,2)
		img_of_stone=stone_img[choice]
		stone.return_self(display_width,500+random.randrange(10,80), stone.width, img_of_stone)
	check=cloud.move()
	if not check:
		choice=random.randrange(0,2)
		img_of_cloud=cloud_img[choice]
		cloud.return_self(display_width,random.randrange(10,200), stone.width, img_of_cloud)
def draw_dino():
	global img_counter
	if img_counter==25:
		img_counter=0
	display.blit(dino_img[img_counter//5],(user_x, user_y))
	img_counter+=1
def print_text(message,x,y,font_color=(0,0,0),font_type='PingPong.ttf',font_size=30):
	font_type=pygame.font.Font(font_type,font_size)
	text=font_type.render(message,True,font_color)
	display.blit(text,(x,y))

def check_collision(barriers):
	for barrier in barriers:
		if user_y + user_height>=barrier.y:
			if barrier.x<=user_x<=barrier.x+barrier.width:
				return True
			elif barrier.x<=user_x+user_width<=barrier.x+barrier.width:
				return True
	return False
def game_over():
	stoped=True
	while stoped:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
		print_text('Game is over. Press Enter to play again. Esc to exit',20,300)
		keys=pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			return True
		if keys[pygame.K_ESCAPE]:
			return False
		pygame.display.update()
		clock.tick(15)
while run_game():
	pass
pygame.quit()
quit()