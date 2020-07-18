import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
import socket
import threading
import time
import tkinter as tk
from tkinter import simpledialog
from playsound import playsound

HEADER = 32
PORT = 5050
SERVER = "192.168.191.216"  #Zero-Tier Server IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

ROOT = tk.Tk()
ROOT.withdraw()
username = simpledialog.askstring(title="Tic Tac Toe (Slave)", prompt="What's your Name?:")

pygame.init()
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH,HEIGHT))

ticks = pygame.transform.scale(pygame.image.load(os.path.join("images", "tick.png")),(int(0.18*WIDTH),int(0.18*HEIGHT)))
cross = pygame.transform.scale(pygame.image.load(os.path.join("images", "cross.png")),(int(0.18*WIDTH),int(0.18*HEIGHT)))

TITLE_FONT = pygame.font.SysFont('comicsans', 60)
USER_FONT = pygame.font.SysFont('comicsans', 50)

gamelist = ["-", "-", "-","-", "-", "-","-", "-", "-"]
current_user = 0
self_no = 0
score_user1 = 0
score_user2 = 0
username1 = ""
username2 = ""
disconnected_check = False

def draw_window(gamelist, a, c):
    global score_user1, score_user2
    
    win.fill(WHITE)
    text = TITLE_FONT.render("Tic Tac Toe", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    pygame.draw.line(win, BLACK, (0.2*WIDTH, 0.4*HEIGHT), (0.8*WIDTH, 0.4*HEIGHT), 4)    #horizontal
    pygame.draw.line(win, BLACK, (0.2*WIDTH, 0.6*HEIGHT), (0.8*WIDTH, 0.6*HEIGHT), 4)
    pygame.draw.line(win, BLACK, (0.4*WIDTH, 0.2*HEIGHT), (0.4*WIDTH, 0.8*HEIGHT), 4)     #vertical
    pygame.draw.line(win, BLACK, (0.6*WIDTH, 0.2*HEIGHT), (0.6*WIDTH, 0.8*HEIGHT), 4)
    if current_user == 0:
        user1 = USER_FONT.render(username1 + ": " + str(score_user1), 1, GREEN)
        user2 = USER_FONT.render(username2 + ": " + str(score_user2), 1, BLACK)
    else:
        user1 = USER_FONT.render(username1 + ": " + str(score_user1), 1, BLACK)
        user2 = USER_FONT.render(username2 + ": " + str(score_user2), 1, RED)
        
    col = 1
    row = 1
    for lists in gamelist:
        if lists == "T":
            win.blit(ticks, (int((0.20*col + 0.01)*WIDTH), int((0.20*row + 0.01)*HEIGHT)))
        elif lists == "C":
            win.blit(cross, (int((0.20*col + 0.01)*WIDTH), int((0.20*row + 0.01)*HEIGHT)))
        col += 1
        if col == 4:
            col = 1
            row += 1
            
    if end:
        if winner == 0:
            final = USER_FONT.render(username1 + " WINS, " + username2 + " LOOSE", 1, GREEN)
            score_user1 += 1
            winning_line(a,c)
        elif winner == 1:
            final = USER_FONT.render(username2 + " WINS, " + username1 + " LOOSE", 1, BLACK)
            score_user2 += 1
            winning_line(a,c)
        else:
            final = USER_FONT.render("Match Tied", 1, BLACK)
        win.blit(final, (WIDTH/2 - final.get_width()/2, HEIGHT - 50))
    else:    
        win.blit(user1, (WIDTH/4 - user1.get_width()/2, HEIGHT - 50))
        win.blit(user2, (3*WIDTH/4 - user2.get_width()/2, HEIGHT - 50))
    
    pygame.display.update()
    
def receive_list(client,):
    global gamelist, current_user, disconnected_check
    connected = True
    while connected:
        temp = ""
        while temp is "":
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                temp = client.recv(msg_length).decode(FORMAT)
                if temp == DISCONNECTED_MESSAGE:
                    connected = False
                    disconnected_check = True
                    break

        gamelist = [char for char in temp]
        if current_user == 0:
            current_user = 1
        else:
            current_user = 0
    client.close()

def winning_line(a, c):
    if a == 0 and c == 2:
        pygame.draw.line(win, RED, (0.2*WIDTH, 0.3*HEIGHT), (0.8*WIDTH, 0.3*HEIGHT), 8)
    elif a == 3 and c == 5:
        pygame.draw.line(win, RED, (0.2*WIDTH, 0.5*HEIGHT), (0.8*WIDTH, 0.5*HEIGHT), 8)
    elif a == 6 and c == 8:
        pygame.draw.line(win, RED, (0.2*WIDTH, 0.7*HEIGHT), (0.8*WIDTH, 0.7*HEIGHT), 8)
        
    if a == 0 and c == 6:
        pygame.draw.line(win, RED, (0.3*WIDTH, 0.2*HEIGHT), (0.3*WIDTH, 0.8*HEIGHT), 8)
    elif a == 1 and c == 7:
        pygame.draw.line(win, RED, (0.5*WIDTH, 0.2*HEIGHT), (0.5*WIDTH, 0.8*HEIGHT), 8)
    elif a == 2 and c == 8:
        pygame.draw.line(win, RED, (0.7*WIDTH, 0.2*HEIGHT), (0.7*WIDTH, 0.8*HEIGHT), 8)
    
    if a == 0 and c == 8:
        pygame.draw.line(win, RED, (0.2*WIDTH, 0.2*HEIGHT), (0.8*WIDTH, 0.8*HEIGHT), 8)
    elif a == 2 and c == 6:
        pygame.draw.line(win, RED, (0.8*WIDTH, 0.2*HEIGHT), (0.2*WIDTH, 0.8*HEIGHT), 8)

def end_screen():
    win.fill(WHITE)
    text = TITLE_FONT.render("Tic Tac Toe", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    if score_user1 > score_user2:
            win_final = USER_FONT.render(username1 + " WINS" , 1, GREEN)
            loose_final = USER_FONT.render(username2 + " LOOSE", 1, RED)
            win.blit(win_final, (WIDTH/2 - win_final.get_width()/2, HEIGHT/2-50))
            win.blit(loose_final, (WIDTH/2 - loose_final.get_width()/2, HEIGHT/2+50))
    elif score_user2 > score_user1:
            win_final = USER_FONT.render(username2 + " WINS" , 1, GREEN)
            loose_final = USER_FONT.render(username1 + " LOOSE", 1, RED)
            win.blit(win_final, (WIDTH/2 - win_final.get_width()/2, HEIGHT/2-50))
            win.blit(loose_final, (WIDTH/2 - loose_final.get_width()/2, HEIGHT/2+50))
    else:
        final = USER_FONT.render("Series Tied!", 1, BLACK)
        win.blit(final, (WIDTH/2 - final.get_width()/2, HEIGHT/2))
    pygame.display.update()
    
    if score_user1 > score_user2:
            if username == username1:
                playsound(os.path.join("music", "applause.wav"))
            else:
                playsound(os.path.join("music", "boo.wav"))
    elif score_user2 > score_user1:
            if username == username2:
                playsound(os.path.join("music", "applause.wav"))
            else:
                playsound(os.path.join("music", "boo.wav"))
    time.sleep(2)

def game():
    global current_user, gamelist, winner, end, self_no, score_user1, score_user2, username1, username2, disconnected_check
    winner = 2
    clock = pygame.time.Clock()
    gamelist = ["-", "-", "-","-", "-", "-","-", "-", "-"]
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    run = True
    end = False
    thread = threading.Thread(target = receive_list, args=(client,))
    thread.start()
    a,b,c = (0,0,0)
    while run: 
        clock.tick(FPS)
        for char in gamelist:
            if char == "-":
                end = False
                break
            else:
                end = True
        if disconnected_check:
            end_screen()
            pygame.quit()
        for sel in wins:
            a,b,c = sel
            if gamelist[a] == gamelist[b] == gamelist[c]:
                if gamelist[a]=="T":
                    winner = 0
                    end = True
                    break
                elif gamelist[b]=="C":
                    winner = 1
                    end = True
                    break
                
        draw_window(gamelist,a,c)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen()
                send(DISCONNECTED_MESSAGE)
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                counter = 0
                for row in range(0,3):
                    for col in range(0,3):
                        if m_x / WIDTH > 0.2*(col+1) and m_x / WIDTH < (0.2*(col+1) + 0.2) and m_y / HEIGHT > 0.2*(row+1) and m_y / HEIGHT < (0.2*(row+1) +0.2) and gamelist[counter] == "-" and winner == 2: 
                            if current_user == 0 and self_no == 0:
                                gamelist[counter] = "T"
                                current_user = 1  
                                send(gamelist, True)    
                            if current_user == 1 and self_no == 1:
                                gamelist[counter] = "C"
                                current_user = 0
                                send(gamelist, True)
                        counter +=1
        if end == True:
            if end == True:
                if end == True:
                    if winner == self_no:
                        playsound(os.path.join("music", "explosion.wav"))
                    else:
                        playsound(os.path.join("music", "crying.wav"))
            time.sleep(2)
            end = False
            gamelist = ["-", "-", "-","-", "-", "-","-", "-", "-"]
            winner = 2
            username = username2
            username2 = username1
            username1 = username
            score_user = score_user1
            score_user1 = score_user2
            score_user2 = score_user
            current_user = 0
            if self_no == 0:
                self_no = 1
            else:
                self_no = 0
   
def send(msg, list_check = False):
    msg_modif = ""
    if list_check:
        for x in msg: 
            msg_modif += x
    else:
        msg_modif = msg
    message = msg_modif.encode(FORMAT)
    send_length = str(len(message)).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))

    client.send(send_length)
    client.send(message)

    
def receive(list_check = False):
    temp = ""
    while temp is "":
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            temp = client.recv(msg_length).decode(FORMAT)

    if list_check:
        return [char for char in temp]
    else:
        return temp    

                       
def main():
    global username1, username2, self_no
    
    pygame.display.set_caption("Tic Tac Toe (Slave)!")
    send(username, False)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    username1 = receive()
    username2 = receive() 
    
    if username == username1:
        self_no = 0
    else:
        self_no = 1  
        
    game()
        
main()