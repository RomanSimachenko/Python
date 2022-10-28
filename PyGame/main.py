# Pygame шаблон - скелет для нового проекта Pygame
import pygame

# Цвета (R, G, B)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
YELLOW = (225, 225, 0)
GRAY = (125, 125, 125)
PINK = (230, 50, 230)

Scircle=(50,50)
R=10

WIDTH = 300  # ширина игрового окна
HEIGHT = 300 # высота игрового окна
FPS = 30 # частота кадров в секунду

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # звук
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.draw.circle(screen,BLACK,Scircle,R)
pygame.display.set_caption("My Game")
clock=pygame.time.Clock()


# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)	
    
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    # Обновление
    
    # Рендеринг
    screen.fill(WHITE)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()