import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.1.20", 7000))
server.listen()
print("waiting for connection-----------")

client , address =server.accept()
print("connection established------------")



while True:
    try:
        data = client.recv(1024).decode()
        
        print(data)
    except:
        client.close()
        
        break  
print("disconnect")



