import random
import time
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
                             height=400)
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
        menu.add_cascade(label='Test', menu=debug)
        
        
        #mouse_input
        self.canvas.bind_all('<Button-1>', self.click)
        
        #player stuff
        self.passed = False
        self.add_two = False
        self.turn = False
        self.cards = []
        self.highest = None #(combination, player)
        self.last_click = None
        self.status = None

        #init op false normaal dit zou alles spel/click commands moeten starten
        self.started = True 

    def loop(self):
        while 1:
            try:
                self.tk.update()
                self.tk.update_idletasks()
                time.sleep(.15)
            except:
                return
            
        

    def set_cards(self, cards):
        self.cards = sorted(cards, key=lambda x: presi_func.values[x])
        self.cardlocs = {}
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
        self.tk.update()
        
    def click(self, evt):
        if not self.started:
            return
        y = self.tk.winfo_pointery() - self.tk.winfo_rooty()
        if y < 350:
            return
        x = self.tk.winfo_pointerx() - self.tk.winfo_rootx()
        for card in self.cardlocs.keys():
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
        if self.highest:
            hand = self.cards.count(card)*[card]
            if presi_func.check(hand, self.highest[0]):
                self.delete_cards(card)
            else:
                return False
        else:
            self.delete_cards(card)

        self.send(hand)
        return True
        
    def delete_cards(self, card):
        self.cards = [i for i in self.cards if (i!=card)]
        print(self.cards)
        for item in self.cardlocs[card][1]:
            self.canvas.delete(item)
        del self.cardlocs[card]

    #buttons on screen 'forever'
    def pas(self):
        self.passed = True
        self.send("pass")

    def two(self):
        self.add_two = True

    #networking host
    def host_setup(self):
        
        if not self.status:
            port = 6567 #todo add custom port
            try:
                int(self.players = input('number of players: '))
            except Exception as e:
                print('STARTUP FAILED')
                print(e)
                return

            self.status = True
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('0.0.0.0', port))
            print('server running on port: ', port)
            self.h_thread = threading.Thread(target=self.server)
            self.h_thread.deamon = True
            #start thread
            self.h_thread.start()
            

    #server
    def server(self):
        

    

    def dumb2(self):
        print('d2')
        self.l.pack_forget()
        self.tk.update()
        
    #networking
    def send(self, msg):
        if self.status == 'host':
            pass
        else:
            #self.status == 'client'
            pass
    

    def destroy(self):
        self.tk.destroy()

a = window()
a.set_cards(['2', '3', 'K', '3', '6', '3', '7', '3', 'Q', '10', '7', '9', '6'])

a.loop()

