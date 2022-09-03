from cmath import rect
from tkinter import font
from turtle import width
import pygame
import os
from random import randint

pygame.init()

#Variaveis
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, "images")
pontos = 3
font = pygame.font.SysFont('fonts/PixelGameFonte', 50)
# posição inicial do dragon e inimigo
pox = 50
poy = 50

triggered = False

poxx = pox -7
poyy = poy 
vel_fire = 0

pos_obj_x = 1350
pos_obj_y = 600

# Tela
x = 1280
y = 720

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('Meu primeiro jogo em python')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'MudWyvernIdleSide.png')).convert_alpha()
sprite_sheet2 = pygame.image.load(os.path.join(diretorio_imagens, 'Jumping_Small_Iceball_14x41.png')).convert_alpha()
bg = pygame.image.load('images/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

obj = pygame.image.load('images/flappy.png').convert_alpha()
obj = pygame.transform.scale(obj, (70, 50))
obj = pygame.transform.rotate(obj, -90)
obj_rect = obj.get_rect()

# Classes responsáveis por mapear as spritesheets

class Dragon(pygame.sprite.Sprite):
    
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    

        self.imagens_dragon = []
        for i in range(4):
            img = sprite_sheet.subsurface((i*48,0), (48,48)) # Sprite com 4 etapas em somente uma direção 48x48
            
            self.imagens_dragon.append(img)
       
        self.index_lista = 0
        self.image = self.imagens_dragon[self.index_lista]
        self.rect = self.image.get_rect()
        
       
    def update(self, pos_x, pos_y):
        
        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dragon[int(self.index_lista)]
        self.rect.center = (pos_x, pos_y)
        
class Fire(pygame.sprite.Sprite):
    
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    

        self.imagens_dragon = []
        for i in range(4):
            img = sprite_sheet2.subsurface((i*14,82), (14,41)) # Sprite com 4 etapas em somente uma direção 48x48
            img = pygame.transform.rotate(img, -90)
            self.imagens_dragon.append(img)
       
        self.index_lista = 0
        self.image = self.imagens_dragon[self.index_lista]
        self.rect = self.image.get_rect()
        
       
    def update(self, pos_x, pos_y):
        
        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dragon[int(self.index_lista)]
        self.rect.center = (pos_x, pos_y)
            
        
# Agrupando o Spritesheet
tds_asspts = pygame.sprite.Group()
fire = Fire()
tds_asspts.add(fire)

todas_as_sprites = pygame.sprite.Group()
dragon = Dragon()
todas_as_sprites.add(dragon)
dragon_rect = dragon

# define as cordenada de respawn do inimigo
def respawn():
    x = 1350
    y = randint(1, 720)
    return [x,y]
#define os parametros de colisão
def colisions():
    drg = dragon.rect
    fr = fire.rect
    
    global pontos
    if  drg.colliderect(obj_rect) or obj_rect.x == 60:
        pontos -= 1
        return True
    elif  fr.colliderect(obj_rect):
        pontos += 1
        return True
    else:
        return False



rodando = True
relogio=pygame.time.Clock()
while rodando:
    
    relogio.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    
    screen.blit(bg, (0,0))

    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x,0))
    
    if pos_obj_x == 50 or colisions():
        pos_obj_x = respawn()[0]
        pos_obj_y = respawn()[1]
    
    # perseguição
    if pos_obj_x != pox:
        pos_obj_x -= 3  + (10 % pontos)
        if pos_obj_y > poy:
            pos_obj_y -= 1 + (pontos% 10)
        elif pos_obj_y < poy:
            pos_obj_y += 1 
    if poxx == pos_obj_x:
        if poyy == pos_obj_y:
            pos_obj_x = respawn()[0]
            pos_obj_y = respawn()[1]
    
    # Teclas
    tecla = pygame.key.get_pressed()
    
    if tecla[pygame.K_UP] and poy > 1:
       poy = poy - 4
       if not triggered:
        poyy = poyy -4
    
    if tecla[pygame.K_DOWN] and poy < 720:
        poy = poy +4
        if not triggered:
            poyy = poyy +4
    
    if tecla[pygame.K_LEFT] and pox > 1:
       pox = pox - 2
       if not triggered:
        poxx = poxx - 2

    if tecla[pygame.K_RIGHT] and pox < 1280:
        pox = pox +2
        if not triggered:
            poxx = poxx +2

    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_fire = 8 + (pontos % 10)
    
    
    #respawn do fogo

    def respawn_fire():
            triggered = False
            respawn_fire_x = pox - 7
            respawn_fire_y = poy
            vel_fire = 0
            
            return [respawn_fire_x, respawn_fire_y, triggered, vel_fire, ]
   
    if poxx - pox > 300 + (pontos % 2): # Alcançe da bola de fogo
        
        poxx, poyy, triggered, vel_fire = respawn_fire()
    

    # Movimento
    x-=3
    poxx += vel_fire
    
    #retangulos de colisão
    obj_rect.x = pos_obj_x
    obj_rect.y = pos_obj_y
    
    score = font.render(f'Pontos: {int(pontos)}', True, (0,0,0))
    screen.blit(score, (50,50))

    tds_asspts.draw(screen)
    tds_asspts.update(poxx, poyy)
    
    todas_as_sprites.draw(screen)
    todas_as_sprites.update(pox,poy)
    
    screen.blit(obj,(pos_obj_x, pos_obj_y))

    pygame.display.update()
