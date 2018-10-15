import random
import time
import socket
import threading
import presi_func
from tkinter import *


class window:
    def __init__(self):
        #screen stuff
        self.tk = Tk()
        self.tk.geometry('800x400')
        self.tk.wm_attributes('-topmost', 1)
        self.tk.resizable(0,0)
        self.tk.title('PRESIDENTEN')
        self.tk.update()
        self.canvas = Canvas(self.tk,
                             width=800,
                             height=400,
                             bd=0,
                             highlightthickness=0)
        self.canvas.place(x=0, y=0)
        
        b_p = Button(self.tk,
                     text='pas',
                     width=5,
                     command=self.pas,
                     font=('Calibri', 12))
        b_p.place(relx=.93, rely=.9)
        b_2 = Button(self.tk,
                     text='add 2',
                     width=5,
                     command=self.two,
                     font=('Calibri', 12))
        b_2.place(relx=.93, rely=.82)        
        self.tk.update()

        
        #drop_down menu
        menu = Menu(self.tk)
        self.tk.config(menu=menu)
        debug = Menu(menu)
        debug.add_command(label='setup host', command=self.host_setup)
        debug.add_command(label='setup join', command=self.join_setup)
        debug.add_command(label='close', command=self.destroy)
        debug.add_command(label='verwerk', command=self.dumb)
        menu.add_cascade(label='Test', menu=debug)

        self.draw()
        
        
        #mouse_input
        self.canvas.bind_all('<Button-1>', self.click)
        
        #player stuff
        self.twos = 0
        self.turn = False #change
        self.cards = []
        self.highest = None #(combination, player)
        self.players = {} #name:[plob number, num of cards]
        self.last_click = None
        self.status = None
        self.cardlocs = {}      

        self.data = None

        #init loop
        #self.loop()

    def draw(self):
        self.plob = {}
        self.plob[1]=[self.canvas.create_text(
                          50, 20, text='player', font=('helvetica',12)),
                      self.canvas.create_rectangle(
                          30, 35, 70, 95, fill='#abcabc'),
                      self.canvas.create_text(
                          50, 50, text='NA', font=('helvetica',12)),
                      self.canvas.create_polygon(
                          40, 0, 60, 0, 50, 15, fill='red',
                          state='hidden')]
        #player 2
        self.plob[2]=[self.canvas.create_text(
                          50, 130, text='player', font=('helvetica',12)),
                      self.canvas.create_rectangle(
                          30, 145, 70, 205, fill='#abcabc'),
                      self.canvas.create_text(
                          50, 160, text='NA', font=('helvetica',12)),
                      self.canvas.create_polygon(
                          40, 110, 60, 110, 50, 125, fill='red',
                          state='hidden')]
        #player 3
        self.plob[3]=[self.canvas.create_text(
                          50, 240, text='player', font=('helvetica',12)),
                      self.canvas.create_rectangle(
                          30, 255, 70, 315, fill='#abcabc'),
                      self.canvas.create_text(
                          50, 270, text='NA', font=('helvetica',12)),
                      self.canvas.create_polygon(
                          40, 220, 60, 220, 50, 235, fill='red',
                          state='hidden')]
        #kader hoogste hand
        self.canvas.create_rectangle(250, 100, 550, 200, fill='#abcabc')
        #info widget + kaarten
        self.info = [self.canvas.create_text(
            0, 400, text='waiting', font=('Helvetica', 10),
            anchor='sw', fill='#10dd00'),
                     self.canvas.create_text(
            255, 100, font=('Helvetica', 10), anchor='nw')]
        #kaarten voorlopig onzichtbaar
        for i in range(8):
            self.info.append(
                [self.canvas.create_rectangle(
                    255+i*37, 120,
                    287+i*37, 190,
                    fill='#ffffff',
                    state='hidden'),#hidden
                self.canvas.create_text(
                    260+i*37, 125,
                    text='10',
                    anchor='nw',
                    state='hidden')])#hidden
        
        self.tk.update()


    def loop(self):
        while 1:
            try:
                self.tk.update()
                self.tk.update_idletasks()
                time.sleep(1/60)
                if self.data:
                    self.verwerk(self.data)
                    self.data = None
            except Exception as e:
                print(e)
                break
        
        

    def set_cards(self, cards):
        self.cards = sorted(cards, key=lambda x: presi_func.values[x])
        card_width = 600/len(self.cards)
        for i, j in enumerate(self.cards):
            ca = self.canvas.create_rectangle(100+i*card_width,
                                              350,
                                              100+(i+1)*card_width,
                                              400,
                                              fill='#ffffff')
            ct = self.canvas.create_text(110+i*card_width,
                                         360,
                                         font=('Helvetica',15),
                                         anchor='nw',
                                         text=j,
                                         fill='#ff0000' if (j=='2') else '#000000')
            
            if j in self.cardlocs.keys():
                self.cardlocs[j][0][1] = 100+(i+1)*card_width
                self.cardlocs[j][1]+=[ca, ct]
            else:
                self.cardlocs[j] = [[100+i*card_width, 100+(i+1)*card_width],
                                    [ca, ct]]          
        for i,j in self.info[2:]:
            self.canvas.itemconfig(i, state='hidden')
            self.canvas.itemconfig(j, state='hidden')
        self.tk.update()

    def delete_all(self):
        for i in self.cardlocs.keys():
            for j in self.cardlocs[i][1]:
                self.canvas.delete(j)
        self.cardlocs = {}
        self.cards = []
        print(self.cardlocs)
        
    def click(self, evt):
        if not self.turn:
            return
        y = self.tk.winfo_pointery() - self.tk.winfo_rooty()
        if y < 350:
            return
        x = self.tk.winfo_pointerx() - self.tk.winfo_rootx()
        for card in self.cardlocs.keys():
            if card == '2':
                continue
            i, j = self.cardlocs[card][0]
            if i<x<j:
                if card == self.last_click:
                    #could be shorter 
                    self.last_click = None
                    for rect in self.cardlocs[card][1][::2]:
                        self.canvas.itemconfig(rect, fill='#ffffff')
                    if not self.check(card):
                        #send message to player: not valid
                        pass
                    break
                elif self.last_click:
                    for rect in self.cardlocs[self.last_click][1][::2]:
                        self.canvas.itemconfig(rect, fill='#ffffff')
                    self.last_click = card
                    for rect in self.cardlocs[card][1][::2]:
                        self.canvas.itemconfig(rect, fill='#ccffff')
                else:
                    self.last_click = card
                    for rect in self.cardlocs[card][1][::2]:
                        self.canvas.itemconfig(rect, fill='#ccffff')
                self.tk.update()

    def check(self, card):
        #todo add 2 support
        hand = ['2']*self.twos + self.cards.count(card)*[card]
        print(self.highest)
        if self.highest:
            if presi_func.check(hand, self.highest[0]):
                print(self.highest[0])
                self.highest = (hand, 'player') #(combination, player)
                self.delete_cards(card)
            else:
                return False
        else:
            self.highest = (hand, 'player') #(combination, player)
            self.delete_cards(card)

        self.send(hand)
        return True
        
    def delete_cards(self, card):
        self.cards = [i for i in self.cards if (i!=card)]
        for item in self.cardlocs[card][1]:
            self.canvas.delete(item)
        del self.cardlocs[card]
        if self.twos:
            for item in range(2*self.twos):
                self.canvas.delete(self.cardlocs['2'][1][item])
            self.cardlocs['2'][1] = self.cardlocs['2'][1][2*self.twos:]
            self.cards = self.cards[self.twos:]
            self.twos = 0 #reset var
                                                    

    #buttons on screen 'forever'
    def pas(self):
        self.turn = False
        self.send('0')

    def two(self):
        self.counter_2 = self.cards.count('2')
        if self.counter_2 == 0:
            print('no two cards')
            return
        self.twos +=1
        if self.twos > self.counter_2:
            self.twos = 0
        if self.twos == 0:
            for card in self.cardlocs['2'][1][::2]:
                self.canvas.itemconfig(card, fill='#ffffff')
        else:
            card = self.cardlocs['2'][1][2*self.twos-2]
            self.canvas.itemconfig(card, fill='#ccffff')
            
        self.tk.update()
        
    #networking host
    def host_setup(self):
        if 1:
            return 
        #begin eerst met de luister methode
##        if not self.status:
##            port = 6567 #todo add custom port
##            try:
##                players = int(input('number of players: '))
##            except Exception as e:
##                print('STARTUP FAILED')
##                print(e)
##                return
##
##            self.status = True
##            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##            self.socket.bind(('0.0.0.0', port))
##            self.socket.listen(1)
##            print('server running on port: ', port)
##            self.h_thread = threading.Thread(target=self.server, args=(players,))
##            self.h_thread.deamon = True
##            #start thread
##            self.h_thread.start()
            
    #networking joiner
    def join_setup(self):
        if not self.status:
            port = 6567 #todo add custom port
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.j_thread = threading.Thread(target=self.listener)
            self.j_thread.deamon = True
            self.j_thread.start()
    
    #server
    def server(self, players):
        self.players = {} #ip:[conn, ip, number of cards, passed]
        for i in range(players):
            con, addr = self.socket.accept()
            print('player %s(%s, %s) joined' %(i+1, conn, addr))
        print(self.players)

        
        self.h_thread.join()
    

    def dumb(self):
        a = input('>')
        try:
            self.verwerk(a)
        except Exception as e:
            print(e)
        #self.l.pack_forget()
        #self.tk.update()
        #
    #networking
    def listener(self):
        ip_host = None
        while not ip_host:
            ip_host = input('ip host: ')
            try:
                ip_host = socket.gethostbyname(ip_host)           
            except:
                print('invalid ip')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #not necessary
        try:
            name = 'success! '+input('name: ')
            self.socket.connect((ip_host, 6567))
            self.socket.send(name.encode()) #controle stuur naam speler
            #start listening
            while True:
                data = self.socket.recv(128) #arbitrair getal
                if not data:
                    break
                data = data.decode()
                if data == '9': break
                self.data = data
        except Exception as e:
            print(e)
        finally:
            self.socket.close()
            self.status = None
            print('connection closed')
            self.turn = False #close interaction
    
    def send(self, hand):
        print('test')
        if self.status == 'host':
            pass
        else:
            #self.status == 'client'
            if hand != '0':
                msg = str(len(hand))+''.join(hand) #list -> string
            else:
                msg = hand
            self.socket.send(msg.encode())
            print('sended ', msg)

    def verwerk(self, data):
        print(len(data), data)
        print(data[0])
        if data[0] == '0':
            #set playernames + num of cards
            #06player13 ->0+(len player name+1)+num of cards
            j = int(data[1:3])
            data = data[3:]
            self.players[data[0:j]] = [1, int(data[j:j+2])]
            data = data[j+2:]
            j = int(data[0:2])
            self.players[data[2:j+2]] = [2, int(data[j+2:j+4])]
            data = data[j+4:]
            j = int(data[0:2])
            self.players[data[2:j+2]] = [3, int(data[j+2:j+4])]
            for i,j in enumerate(list(self.players.keys())):
                i+=1
                self.canvas.itemconfig(self.plob[i][0],
                                       text=j)
                self.canvas.itemconfig(self.plob[i][2],
                                       text=self.players[j][1])
                self.tk.update()
       
        elif data[0] == '1':
            if data[1] == '1':
                if len(self.cards) == 0:
                    self.send('0')
                    
                self.turn = True
                self.canvas.itemconfig(self.info[0], text='Your turn')
            else:
                self.canvas.itemconfig(
                    self.plob[self.players[data[2:]][0]][3],
                    state='normal')
                
                
        elif data[0] == '2':
            j = int(data[1]) #len of cards
            #width = 30, heigth=70
            if j == 0:
                #vorige persoon heeft gepast
                pass
            else:
                for i, (k, t) in enumerate(self.info[2:j+2]):
                    self.canvas.itemconfig(k, state='normal')
                    kaart = data[i+2]
                    self.canvas.itemconfig(
                        t, state='normal', text=kaart,
                        fill='#ff0000' if (kaart=='2') else '#000000')
                self.highest = [data[2:j+2], data[j+2:]]
                print(self.highest)
                data = data[j+2:]
                self.highest[1] = data
                self.canvas.itemconfig(self.info[1],
                                       text=data)
                self.players[data][1] -= j
                self.canvas.itemconfig(
                    self.plob[self.players[data][0]][2],
                    text=self.players[data][1])
                self.canvas.itemconfig(
                    self.plob[self.players[data][0]][3],
                    state='hidden')
        elif data[0] == '3':
            #set cards:
            self.delete_all()
            self.set_cards([i for i in data[1:]])
            for i in self.plob.keys():
                self.canvas.itemconfig(self.plob[i][2], text=13)       
        else:
            return False
                
                                       

    def destroy(self):
        self.tk.destroy()

a = window()
#a.set_cards(['2', '2', 'K', '3', '6', '3', '7', '3', 'Q', '10', '7', '9', '6'])

a.loop()
