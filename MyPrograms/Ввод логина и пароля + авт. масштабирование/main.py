from data import config as cfg
import pygame,sys,os,random,ctypes
pygame.init()
clock=pygame.time.Clock()
percent=cfg.percent
def print_text(text,x,y,font_color=(0,0,0),font_type=r'data\Fonts\PingPong.ttf',font_size=percent):
	font_type=pygame.font.Font(font_type,font_size)
	text=font_type.render(text,True,font_color)
	display.blit(text,(x,y))
def colors():
	global WHITE,BLACK,RED,GREEN,BLUE
	WHITE=(255,255,255)
	BLACK=(0,0,0)
	RED=(255,0,0)
	GREEN=(0,255,0)
	BLUE=(0,0,255)
colors()
def display():
	global display,display_width,display_height
	display_info=pygame.display.Info()
	if 800<=cfg.width<=1920:
		display_width=cfg.width
	else:
		display_width=display_info.current_w
	if 600<=cfg.height<=1080:
		display_height=cfg.height
	else:
		display_height=display_info.current_h
	display_width,display_height=display_width*percent//100,display_height*percent//100
	display=pygame.display.set_mode((display_width,display_height))
	pygame.display.set_caption("Крестики-нолики")
display()
def button1_settings():
	global button1_width,button1_height,button1_x,button1_y
	button1_width=600
	button1_height=150
	button1_width,button1_height=button1_width*percent//100,button1_height*percent//100
	button1_x=display_width//2-button1_width//2
	button1_y=display_height//2
button1_settings()
def load():
	global background1,button1_log_in,button1_register,button12_log_in,button12_register,exit1,log_in_register,button_log_in_and_register,button_continue,button_continue1
	background1=pygame.image.load(r'data\sprites\main_menu1.png')
	background1=pygame.transform.scale(background1,(display_width,display_height))
	button1_log_in=pygame.image.load(r'data\sprites\button1_log_in.png')
	button1_register=pygame.image.load(r'data\sprites\button1_register.png')
	button12_log_in=pygame.image.load(r'data\sprites\button12_log_in.png')
	button12_register=pygame.image.load(r'data\sprites\button12_register.png')
	button1_log_in,button1_register=pygame.transform.scale(button1_log_in,(button1_width,button1_height)),pygame.transform.scale(button1_register,(button1_width,button1_height))
	button12_log_in,button12_register=pygame.transform.scale(button12_log_in,(button1_width,button1_height)),pygame.transform.scale(button12_register,(button1_width,button1_height))
	exit1=pygame.image.load(r'data\sprites\exit1.png')
	exit1=pygame.transform.scale(exit1,(100*percent//100,100*percent//100))
	log_in_register=pygame.image.load(r'data\sprites\log_in_register.png')
	log_in_register=pygame.transform.scale(log_in_register,(display_width,display_height))
	button_log_in_and_register=pygame.image.load(r'data\sprites\log_in_register_button.png')
	button_log_in_and_register=pygame.transform.scale(button_log_in_and_register,(button1_width,button1_height))
	button_continue=pygame.image.load(r'data\sprites\button_continue.png')
	button_continue=pygame.transform.scale(button_continue,(660*percent//100,165*percent//100))
	button_continue1=pygame.image.load(r'data\sprites\button_continue1.png')
	button_continue1=pygame.transform.scale(button_continue1,(660*percent//100,165*percent//100))
load()
def check_capslock():
	global capslock_act
	hllDll=ctypes.WinDLL("User32.dll")
	VK_CAPITAL=0x14
	CAPSLOCK=hllDll.GetKeyState(VK_CAPITAL)
	if ((CAPSLOCK) & 0xffff)!=0:
		capslock_act=True
	else:
		capslock_act=False
def check_click1():
	global run
	mouse_x,mouse_y=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if button1_x<=mouse_x<=button1_x+button1_width and button1_y-display_height*25//100<=mouse_y<=(button1_y-display_height*25//100)+button1_height:
		display.blit(button12_log_in,(button1_x,button1_y-display_height*25//100))
		if click[0]==1:
			pygame.time.delay(100)
			run=False
			log_in()
	else:
		display.blit(button1_log_in,(button1_x,button1_y-display_height*25//100))
	if button1_x<=mouse_x<=button1_x+button1_width and button1_y+display_height*15//100<=mouse_y<=(button1_y+display_height*15//100)+button1_height:
		display.blit(button12_register,(button1_x,button1_y+display_height*15//100))
		if click[0]==1:
			pygame.time.delay(100)
			run=False
			register()
	else:
		display.blit(button1_register,(button1_x,button1_y+display_height*15//100))
def log_in_or_register():
	global run
	FPS=30
	run=True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
				sys.exit()
		display.blit(background1,(0,0))
		display.blit(exit1,(display_width*5//100,display_height*5//100))
		check_click1()
		pygame.display.update()
def check_mouse_click():
	global login_act,password_act,login_string,password_string,all_login_symbols,all_password_symbols
	if button1_x<=mouse_x<=button1_x+600*percent//100 and button1_y-display_height*25//100<=mouse_y<=(button1_y-display_height*25//100)+150*percent//100:
		login_string=''
		all_login_symbols=0
		login_act=True
	else:
		if login_string=='':
			login_string='Login'
			all_login_symbols=0
		login_act=False
	if button1_x<=mouse_x<=button1_x+600*percent//100 and button1_y-display_height*10//100<=mouse_y<=(button1_y-display_height*10//100)+150*percent//100:
		password_string=''
		all_password_symbols=0
		password_act=True
	else:
		if password_string=='':
			password_string='Password'
			all_password_symbols=0
		password_act=False
def settings_text():
	global allowed_numbers,allowed_small_symbols,allowed_large_symbols,allowed_others_symbols,exceptions_symbols,login_act,password_act,login_string,password_string,numbers_in_string,small_symbols_in_string,large_symbols_in_string,others_symbols_in_string
	allowed_numbers=[49,50,51,52,53,54,55,56,57,48]
	allowed_small_symbols=[113,119,101,114,116,121,117,105,111,112,97,115,100,102,103,104,106,107,108,122,120,99,118,98,110,109]
	allowed_large_symbols=[81,87,69,82,84,89,85,73,79,80,65,83,68,70,71,72,74,75,76,90,88,67,86,66,78,77]
	allowed_others_symbols=[95,46,45,33,63,60,62,58,59,61]
	exceptions_symbols=[8,1073741881,1073742049]
	numbers_in_string,small_symbols_in_string,large_symbols_in_string,others_symbols_in_string=0,0,0,0
	login_act=False
	password_act=False
	login_string='Login'
	password_string='Password'
settings_text()	
def log_in_continue():
	keys=pygame.key.get_pressed()
	mouse_x,mouse_y=pygame.mouse.get_pos()
	click=pygame.mouse.get_pressed()
	if display_width//2-(660*percent//100)//2<=mouse_x<=display_width//2-(660*percent//100)//2+660*percent//100 \
	and 165*percent//100+display_height*55//100<=mouse_y<=165*percent//100+display_height*55//100+165*percent//100:
		display.blit(button_continue1,((display_width//2-(660*percent//100)//2),165*percent//100+display_height*55//100))
		if click[0]==1:
			log_in_run=False
			game()
	else:
		display.blit(button_continue,((display_width//2-(660*percent//100)//2),165*percent//100+display_height*55//100))
def log_in():
	global login_string,password_string,login_act,password_act,mouse_x,mouse_y,numbers_in_string,small_symbols_in_string,large_symbols_in_string,others_symbols_in_string,all_login_symbols,all_password_symbols,click
	FPS=30
	click=[0]
	login_limit=7
	password_limit=7
	all_login_symbols=0
	all_password_symbols=0
	log_in_run=True
	while log_in_run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
				sys.exit()
			if login_act:
				if all_login_symbols<=login_limit:
					if event.type==pygame.KEYDOWN:
						if capslock_act and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
						elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
						elif capslock_act:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+(chr(event.key).upper())
						else:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_login_symbols+=1
								login_string=login_string+chr(event.key)
			if password_act:
				if all_password_symbols<=password_limit:
					if event.type==pygame.KEYDOWN:
						if capslock_act and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
						elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
						elif capslock_act:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+(chr(event.key).upper())
						else:
							if event.key in allowed_numbers:
								numbers_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_small_symbols:
								small_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_large_symbols:
								large_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
							elif event.key in allowed_others_symbols:
								others_symbols_in_string+=1
								all_password_symbols+=1
								password_string=password_string+chr(event.key)
		check_capslock()
		keys=pygame.key.get_pressed()
		mouse_x,mouse_y=pygame.mouse.get_pos()
		click=pygame.mouse.get_pressed()
		display.blit(log_in_register,(0,0))
		display.blit(button_log_in_and_register,(button1_x,button1_y-display_height*25//100))
		display.blit(button_log_in_and_register,(button1_x,button1_y-display_height*10//100))
		log_in_continue()
		print_text(login_string,button1_x+15,(button1_y-display_height*25//100)+15,(151,151,151))
		print_text(password_string,button1_x+15,(button1_y-display_height*10//100)+15,(151,151,151))
		if click[0]==1:
			check_mouse_click()
		pygame.display.update()
def register():
	FPS=30
	while True:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
				sys.exit()
		display.blit(log_in_register,(0,0))
		pygame.display.update()
def game():
	FPS=60
	game_run=True
	while game_run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				quit()
				sys.exit()
		display.fill(GREEN)
		print_text('YES',display_width//2,display_height//2)
		pygame.display.update()
log_in_or_register()