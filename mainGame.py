import numpy as np
import pygame
import sys
import math
import random

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

limitMin = 50
limitMax = 650
x = 50
game_over = False
turn = 0


def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def checkfullboard(board):
    for i in range(7):
        if  is_valid_location(board,i):
            return False
    return True

def monte_turn(boarda):
    
    win = [0,0,0,0,0,0,0]
    for i in range(7):
        for x in range(100):
            board = np.copy(boarda)
            turn = 0
            game_over = False
            if is_valid_location(board,i):
                row = get_next_open_row(board, i)
                drop_piece(board, row, i, 2)
                if winning_move(board, 2):
                    win[i] +=1
                    game_over = True
            
            #print("work1")
            while not game_over:
                #pygame.time.wait(10)
                if(checkfullboard(board)):
                    game_over = True
                else:
                    if turn == 0:
                
                        col = int(random.randrange(7))
                        while not is_valid_location(board,col):
                            col = int(random.randrange(7))
                    
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
 
                        if winning_move(board, 1):
                            #label = myfont.render("Player 1 wins!!", 1, RED)
                            #screen.blit(label, (40,10))

                            game_over = True
 
 
                    # # Ask for Player 2 Input
                if checkfullboard(board):
                    game_over = True
                else:
                    if turn==1:               
                        col = int(random.randrange(7))
                        while not is_valid_location(board,col):
                            col = int(random.randrange(7))
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
 
                        if winning_move(board, 2):
                            win[i] +=1
                            game_over = True
 
                #print_board(board)
                draw_board(board)
 
                turn += 1
                turn = turn % 2
    
    #print(win)
    if win == [0,0,0,0,0,0,0]:
        random.randrange(7)
    else:
        return win.index(max(win))
 
def move(dir,color):
    global x
    if dir==0:
        if x-100 >= limitMin:
            x -= 100
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            pygame.draw.circle(screen, color, (x, int(SQUARESIZE/2)), RADIUS)
    elif dir==1:
        if x+100 <= limitMax:
            x += 100
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            pygame.draw.circle(screen, color, (x, int(SQUARESIZE/2)), RADIUS)
            
def drop():
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    global turn, game_over
    if turn == 0:
        col = int(math.floor(x/SQUARESIZE))
    else:
        col = monte_turn(board)
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        if turn == 0:
            drop_piece(board, row, col, 1)
            if winning_move(board, 1):
                label = myfont.render("Player 1 wins!!", 1, RED)
                screen.blit(label, (40,10))
                game_over = True
        else:    
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True
    #print_board(board)
    draw_board(board)
    turn += 1
    turn = turn % 2
    
    if game_over:
        pygame.time.wait(3000)
        

board = create_board()
#print_board(board)
pygame.init()
myfont = pygame.font.SysFont("monospace", 75)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


def playTurn():
    global x
    x = 50
    nextTurn = False
    if turn==0:
        color = RED
    else:
        color = YELLOW
        nextTurn = True
        drop()
    pygame.draw.circle(screen, color, (x, int(SQUARESIZE/2)), RADIUS)
    while nextTurn == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    drop()
                    nextTurn = True
                elif event.key == pygame.K_LEFT: 
                    move(0,color)
                elif event.key == pygame.K_RIGHT:
                    move(1,color)
            pygame.display.update()
    
    
def main():
    while not game_over:
        playTurn()
        

main()