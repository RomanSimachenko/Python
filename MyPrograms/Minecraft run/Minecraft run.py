import math,pygame,random,pymysql.cursors,socket
pygame.init()
Best_score=0
# IP=(socket.gethostbyname(socket.gethostname()))
# def check_ip():
#     global Best_score,IP
#     connection=pymysql.connect(host='localhost',
#                                  user='root',
#                                  password='root1',
#                                  db='bd_test',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor)
#     try:
#             with connection.cursor() as cursor:
#                 sql = "SELECT IP,Best_score FROM test"
#                 cursor.execute(sql)
#                 for row in cursor:
#                     if row['IP']==IP:
#                         Best_score=row['Best_score']
#                         break
#     finally:
#         connection.close()
# check_ip()
def display():
	global display_width,display_height,display
	display_width=1280
	display_height=1000
	display=pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption(r'Minecraft run!')
display()
def load():
	global lava_images,Background,player_images,cloud_images,lian_image,heart_image,menu_fone,menu_button
	player_images=[pygame.image.load(r'data\Sprites\steve2.png'),pygame.image.load(r'Data\Sprites\steve1.png'),pygame.image.load(r'Data\Sprites\steve0.png')]
	Background=pygame.image.load(r'data\Sprites\Background.png')
	lava_images=[pygame.image.load(r'data\Sprites\lava0.png'),pygame.image.load(r'Data\Sprites\lava1.png'),pygame.image.load(r'Data\Sprites\lava2.png')]
	icon=pygame.image.load(r'data\Sprites\icon.jpg')
	cloud_images=[pygame.image.load(r'data\Sprites\cloud1.png'),pygame.image.load(r'data\Sprites\cloud2.png')]
	pygame.display.set_icon(icon)
	lian_image=pygame.image.load(r'data\Sprites\lian.png')
	heart_image=pygame.image.load(r'data\Sprites\heart.png')
	menu_fone=pygame.image.load(r'data\Sprites\menu.png')
	menu_button=pygame.image.load(r'data\Sprites\menu_button.png')
load()
def settings():
	global jump_count,FPS,jump_act,Score,clock,speed_score,d,d1
	clock=pygame.time.Clock()
	Score=0
	jump_count=60
	FPS=100
	jump_act=False
	speed_score=0.07
	d=True
	d1=3
settings()
def sounds():
	global jump_sound,fall_sound,button_sound
	pygame.mixer.music.load(r'data\Sounds\Fone.mp3')
	pygame.mixer.music.set_volume(0.2)
	jump_sound=pygame.mixer.Sound(r'data\Sounds\Rrr.wav')
	fall_sound=pygame.mixer.Sound(r'data\Sounds\Bdish.wav')
	button_sound=pygame.mixer.Sound(r'data\Sounds\Button_sound.wav')
sounds()
def print_text(text,x,y,font_color=(0,0,0),font_type=r'data\Fonts\PingPong.ttf',font_size=40):
	font_type=pygame.font.Font(font_type,font_size)
	text=font_type.render(text,True,font_color)
	display.blit(text,(x,y))
def player_settings():
	global player_count,player_width,player_height,player_x,player_y
	player_count=0
	player_width=102
	player_height=207
	player_x=display_width//3-100
	player_y=display_height-player_height-281
player_settings()
def heart_settings():
	global heart_width,heart_height,heart_x,heart_y,hearts,heart_check,heart_count
	heart_width=60
	heart_height=60
	heart_x=30
	heart_y=150
	hearts=3
	heart_count=0
	heart_check=False
heart_settings()
def create_lava():
	global lava_x,lava_y,lava_width,lava_height,lava,lava_images,lava_speed
	lava_width=161
	lava_height=161
	lava_x=display_width+lava_width+10
	lava_y=display_height-283
	lava=lava_images[0]
	lava_speed=30.0
create_lava()
def delay():
	global d,d1
	d=True
	while d:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
		display.blit(Background,(0,0))
		display.blit(player_images[2],(player_x,player_y))
		print_text('Score:'+str(math.trunc(Score)),30,30)
		print_text('Best score:'+str(math.trunc(Best_score)),30,90)
		display.blit(heart_image,(heart_x,heart_y))
		display.blit(heart_image,(heart_x+65,heart_y))
		display.blit(heart_image,(heart_x+130,heart_y))
		print_text(str(d1),560,250,font_size=300)
		if d1==0:
			d=False
			lava_x=display_width+lava_width+10
		pygame.time.delay(1100)
		d1-=1
		pygame.display.update()
		clock.tick(15)
def menu():
	pygame.mixer.music.play(-1)
	show=True
	while show:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
		mouse_pos=pygame.mouse.get_pos()
		click=pygame.mouse.get_pressed()
		display.blit(menu_fone,(0,0))
		display.blit(menu_button,(450,350))
		if click[0]==1 and 450<mouse_pos[0]<450+310 and 350<mouse_pos[1]<350+314:
			pygame.mixer.Sound.play(button_sound)
			show=False
			delay()
		pygame.display.update()
		clock.tick(15)
menu()
def game():
	global Score,jump_act,run,Best_score,cloud_x,heart_check,hearts,lian_x,number,start_run,d,d1,dl
	pygame.mixer.music.play(-1)
	number=0
	start_run=True
	run=True
	create_lava()
	while run:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				if Score>Best_score:
					file=open(r'data\Best_score.txt','w')
					Best_score=Score
					file.write(str(Best_score))
					file.close()
				pygame.quit()
				quit()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			jump_act=True
		if jump_act:
			jump()
		if keys[pygame.K_ESCAPE]:
			pause()
		Score+=speed_score
		display.blit(Background,(0,0))
		draw_cloud()
		if heart_check:
			heart_blinks()
		elif check_collision():
			pygame.mixer.Sound.play(fall_sound)
			hearts-=1
			heart_check=True
		move_lava()
		lian_move()
		draw_player()
		print_text('Score:'+str(math.trunc(Score)),30,30)
		print_text('Best score:'+str(math.trunc(Best_score)),30,90)
		if Best_score>1 and Score+0.8>Best_score and Score-2<Best_score:
			print_text('NEW RECORD!',400,300,font_color=RED,font_size=80)
		if hearts==0:
			game_over()
			run=False
		draw_heart()
		pygame.display.update()
		clock.tick(FPS)
	return game_over()
def colors():
	global WHITE,BLACK,RED,GREEN,BLUE
	BLACK=(0, 0, 0)
	BLUE=(0, 0, 255)
	WHITE=(255, 255, 255)
	RED=(255, 0, 0)
	GREEN=(0, 255, 0)
colors()
def jump():
	global player_y,jump_act,jump_count
	if jump_count>=-60:
		if jump_count==60:
			pygame.mixer.Sound.play(jump_sound)
		player_y-=jump_count/1
		jump_count-=6
	else:
		jump_count=60
		jump_act=False	
def draw_player():
	global player_count
	if player_count==12:
		player_count=0
	display.blit(player_images[player_count//4],(player_x,player_y))
	player_count+=1
def cloud_settings():
	global cloud_width,cloud_heigth,cloud_x,cloud_y,cloud_image,cloud_choice
	cloud_width=623
	cloud_heigth=221
	cloud_x=display_width+cloud_width+10
	cloud_y=150
	cloud_choice=1
cloud_settings()
def draw_cloud():
	global cloud_x,cloud_images,cloud_y,cloud_image,cloud_choice
	if cloud_choice==1:
		display.blit(cloud_images[0],(cloud_x,cloud_y))
	if cloud_choice==2:
		display.blit(cloud_images[1],(cloud_x,cloud_y))
	if cloud_x>=0-cloud_width-10:
		cloud_x-=10
	else:
		cloud_choice=random.randrange(1,4)
		cloud_x=display_width+cloud_width+10
def move_lava():
	global lava_x,lava_width,lava,lava_speed,speed_score
	display.blit(lava,(lava_x,lava_y))
	if lava_x>=0-lava_width-10:
		lava_x-=lava_speed
	else:
		lava_speed+=0.05
		choice_lava()
		lava_x=display_width+lava_width+10
def choice_lava():
	global lava,lava_images,lava_width
	choice=random.randrange(1,6)
	if choice==1 or choice==3:
		lava=lava_images[0]
		lava_width=161
	elif choice==2 or choice==5:
		lava=lava_images[1]
		lava_width=322
	elif choice==4:
		lava=lava_images[2]
		lava_width=483
def lian_settings():
        global lian_width,lian_height,lian_x,lian_y,lian_speed,spawn_lian
        lian_width=150
        lian_height=350
        lian_x=display_width+lian_width+10
        lian_y=300
        lian_speed=20
        spawn_lian=0
lian_settings()
def lian_move():
        global lian_x,lian_image,lian_y,lian_speed,spawn_lian
        if spawn_lian==1:
        	display.blit(lian_image,(lian_x,lian_y))
        if lian_x>=0-lian_width-10:
                lian_x-=lian_speed
        else:
        	spawn_lian=random.randrange(1,3)
        	lian_x=display_width+lian_width+10
def draw_heart():
	global hearts
	if hearts==3:
		display.blit(heart_image,(heart_x,heart_y))
		display.blit(heart_image,(heart_x+65,heart_y))
		display.blit(heart_image,(heart_x+130,heart_y))
	if hearts==2:
		display.blit(heart_image,(heart_x,heart_y))
		display.blit(heart_image,(heart_x+65,heart_y))
	if hearts==1:
		display.blit(heart_image,(heart_x,heart_y))
def heart_blinks():
	global heart_count,hearts,heart_check
	if heart_count==20:
		heart_count=0
		heart_check=False
	if heart_count%5==0:
		if hearts==2:
			display.blit(heart_image,(heart_x+130,heart_y))
		elif hearts==1:
			display.blit(heart_image,(heart_x+65,heart_y))
	heart_count+=1
def check_collision():
	global run,lava_barriers,lava_x,lava_width,player_x,player_height,player_width
	if not jump_act:
		lava_barriers=[i for i in range(int(lava_x-170),int(lava_x+lava_width-90))]
		if player_x-player_height+player_width in lava_barriers:
			return True
def pause():
	global Score,Best_score
	paused=True
	pygame.mixer.music.pause()
	while paused:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				if Score>Best_score:
					file=open(r'data\Best_score.txt','w')
					Best_score=Score
					file.write(str(Best_score))
					file.close()
				pygame.quit()
				quit()
		print_text('Paused. Press space to continue',300,300)
		keys=pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			paused=False
		pygame.display.update()
		clock.tick(15)
	pygame.mixer.music.unpause()
def game_over():
	global run,Score,Best_score,lava_speed,hearts
	stoped=True
	while stoped:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				if Score>Best_score:
					file=open(r'data\Best_score.txt','w')
					Best_score=Score
					file.write(str(Best_score))
					file.close()
				pygame.quit()
				quit()
		print_text('Game is over. Press enter to play again. Esc to exit',150,300)
		print_text('Your score:'+str(math.trunc(Score)),450,400,font_size=60)
		keys=pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			if Score>Best_score:
				file=open(r'data\Best_score.txt','w')
				Best_score=Score
				file.write(str(Best_score))
				file.close()
			Score=0
			lava_speed=30.0
			hearts=3
			create_lava()
			cloud_settings()
			lian_settings()
			return True
		if keys[pygame.K_ESCAPE]:
			if Score>Best_score:
				file=open(r'data\Best_score.txt','w')
				Best_score=Score
				file.write(str(Best_score))
				file.close()
			return False
		pygame.display.update()
		clock.tick(15)
while game():
	pass
if Score>Best_score:
	file=open(r'data\Best_score.txt','w')
	Best_score=Score
	file.write(str(Best_score))
	file.close()
pygame.quit()
quit()
