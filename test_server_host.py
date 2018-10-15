import socket
import threading
import presi_func


class Host(object):
    '''host for presidenten game'''
    def __init__(self, port):
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv-4, tcp
        self.s.bind(('0.0.0.0', port))
        self.s.listen(1)
        self.connections = {}
        #self.threads = {}

        self.players = []
        self.card_num = {}
        self.passed = []
        
        try:
            #functies
            self.connect()
            self.namen()
            self.loop()
        except Exception as e:
            print(e)
        finally:
            self.s.close()
        '''
        pass

        
    def connect(self, num=4):
        for i in range(num):
            con, addr = s.accept()
            name = con.recv(128).decode()
            #todo add check for duplicate names
            self.connections[name] = [con, addr]
            self.players.append(name)
            '''
            self.threads[name] = threading.Thread(self.listener,
                                                  args=(con,),
                                                  deamon=True)
            self.threads[name].start()
            '''
            print(con, addr)
        print(self.players)

    '''    
    def listener(self, con):
        while 1:
            data = con.recv(128)
            if not data:
                break
            self.data = self.data.decode()
            print(data.decode())
        con.close()

    '''
    def namen(self):
        for i in self.players:
            msg = '0'
            for j in self.players:
                if i == j:
                    continue
                else:
                    if len(j)<10:
                        msg+='0'
                    msg += str(len(j))+j+'13'
            self.connections[i].send(msg.encode())
                  
        
    def loop(self):
        for i, j in enumerate(presi_func.deel()):
            print(i,j)
            hand = '3'+''.join(j)
            print(hand)
            self.connections[self.players[i]].send(hand)
            
            
    

    
    def game(self):
        restart = False
        while not restart:
            for i in self.players:
                if len(self.passed)+1 == len(self.players):
                    #als iedereen gepast en er maar 1 overblijft
                    restart = True
                    break
                elif i in self.passed:
                    continue
                for j in self.players:
                    if i == j:
                        self.connections[j][0].send('11'.encode())
                    else:
                        self.connections[j][0].send(('10'+i).encode())
                data = self.connections[i][0].recv(128).decode()
                if data == '0':
                    self.passed.append(i)
                    continue
                self.card_num[i] -= int(data[0])
                msg = '2'+data+i
                print(msg)
                for j in self.players:
                    self.connections[j][0].send(msg.encode())

        if list(self.cardnum.values()).count(0) == 3:
            return
        for i in self.players:
            if i not in self.passed:
                break
        self.passed = []
        index = self.players.index(i)
        self.players = self.players[index:]+self.players[:index]
        print(self.players)

    def send(self, con, msg):
        con.send(msg.encode())



    def debug(self):
        data = input('')
        if data == 'q':
            '''
            for t in self.threads.keys():
                t.join()
            '''
            self.s.close()
        else:
            pass

    
                
                
    
        

    
'''
def listener(con):
    while 1:
        data = con.recv(128)
        if not data:
            break
        print(data.decode())
    con.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 6567))
s.listen(1)
con, addr = s.accept()
print(con, addr)

thread = threading.Thread(target=listener, args=(con,))
thread.deamon = True
thread.start()


while 1:
    data = input()
    if data == 'q':
        break
    else:
        con.send(data.encode())

thread.join()
s.close()
'''
