import socket
from threading import Thread
from datetime import datetime


file = open(f"chatroom_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt",  "w")
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("192.168.1.20", 5009))
server.listen()
all_clients = {}


def client_thread(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                raise Exception("client disconnected")
            text = msg.decode()
            for c in all_clients:
             if c != client:   
                 c.send(msg)

              
            file.write(f"{all_clients[client]}: {text}\n")
            file.flush() 
        except:
            name = all_clients[client]
            print(f"Connection failed: {name} disconnected")
            for c in all_clients:
                if c != client:
                    c.send(f"{name} has left the chat".encode())
                    file.write(f"{name} has left the chat\n")
            del all_clients[client]
            client.close()
            break

while True:
    print("waiting for connection-----------")
    client , address = server.accept()
    print("connection established")
    name = client.recv(1024).decode()
    all_clients[client] = name
    for c in all_clients:
        if c != client:
           c.send(f"{name} has joind the chat".encode())
           file.write(f"{name} has joind the chat\n")



    thread = Thread(target=client_thread,args=(client,))
    thread.start()





