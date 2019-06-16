#!/usr/bin/python3
#simple tetris game for practise use

import pygame
import sys
import random
import time

block_initial_position = [20, 5]
score = [0]
times = 0
gameover = []
press = False
all_block = [[[0,0],[0,-1],[0,1],[0,2]], [[0,0],[0,1],[-1,1],[-1,0]],\
        [[0,0],[0,-1],[-1,0],[-1,1]],[[0,0],[0,1],[-1,-1],[-1,0]],\
        [[0,0],[1,0],[-1,0],[1,-1]],[[0,0],[1,0],[-1,0],[1,1]]] #six kinds of blocks
background = [[0 for column in range(10)] for row in range(22)]
background[0] = [1 for column in range(10)]
select_block = list(random.choice(all_block)) #randomly select a block

def move(n):
    if n == 100:
        for row, column in select_block:
            pygame.draw.rect(screen, (255,165,0),((column+block_initial_position[1])*40,\
                    800-(row+block_initial_position[0])*40, 38, 38))
        for row in range(20): 
            for column in range(10):
                if background[row][column]:
                    pygame.draw.rect(screen,(0,0,255),(column*40,800-row*40,38,38))

    y_drop, x_move = block_initial_position
    if n == 1 or n == -1:  #update the position for each block while wove x or -x
        x_move += n
        for row,column in select_block:
            if (column+x_move) < 0 or (column+x_move) > 9 or background[row+y_drop][column+x_move]:
                break
            else:
                block_initial_position.clear()
                block_initial_position.extend([y_drop,x_move])
    if n == 0: #anticlockwise rotation 90 degree of block
        rotating_position = [(-column,row) for row,column in select_block]
        for row,column in rotating_position:
            if (column+x_move) < 0 or (column+x_move) > 9 or background[row+y_drop][column+x_move]:
                break
            else:
                select_block.clear()
                select_block.extend(rotating_position)
    if n == 10:
        y_drop -= 1
        for row,column in select_block:
            if background[row+y_drop][column+x_move] == 1:
                break
            else:
                block_initial_position.clear()
                block_initial_position.extend([y_drop,x_move])
                return
        for row,column in select_block:
            background[block_initial_position[0]+row][block_initial_position[1]+column] = 1
        complete_row = []
        for row in range(1,21):
            if 0 not in background[row]:
                complete_row.append(row)
        complete_row.sort(reverse=True)
        for row in complete_row:
            background.pop(row)
            background.append([0 for column in range(10)])
        score[0] += len(complete_row)
        pygame.display.set_caption('Tetris, Score: '+str(score[0])+' Tonymot')
        select_block.clear()
        select_block.extend(list(random.choice(all_block)))
        block_initial_position.clear()
        block_initial_position.extend([20,4])
        for row,column in select_block:
            if background[row+block_initial_position[0]][column+block_initial_position[1]]:
                gameover.append(1)

pygame.init()
screen = pygame.display.set_mode((400,800)) #initialize a window

while True:
    screen.fill((255,255,255)) #fill the whole window with while solid color
    for event in pygame.event.get(): #get the key event
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            move(-1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            move(1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            move(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            press = True   #while press doen key, block move more faster
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            press = False
    if press:
        times += 10
    if times >= 50: #move 10 per 50 times while press down key
        move(10)
        times = 0
    else:
        times += 1
    if gameover:
        sys.exit() 
    move(100)  #create a new tetris per frame
    pygame.time.Clock().tick(200) #the program will never run at more than 200 frams per second
    pygame.display.flip()   #update the whole screen  

