#coding: utf-8

import pygame,time
from pygame.locals import *
from sys import exit

pygame.init()
screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption('first')

background=pygame.image.load('./sushiplate.jpg').convert()
mouse_cursor=pygame.image.load('./fugu.png').convert_alpha()

x,y=200,200
m_x=0

while True:
  for event in pygame.event.get():
    if event.type==QUIT:
      exit()
    if event.type==KEYDOWN:
      if event.key==K_LEFT:
        m_x=-1
      if event.key==K_RIGHT:
        m_x=1
    elif event.type==KEYUP:
      m_x=0
  x+=m_x
  #x,y=pygame.mouse.get_pos()
  screen.blit(background,(0,0))
  screen.blit(mouse_cursor,(x,y))
  pygame.display.update()
