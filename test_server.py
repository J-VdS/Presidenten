import socket
import threading


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
