import socket
import threading




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.1.20", 5000))
server.listen()
print("waiting for connection-----------")


client, address = server.accept()
print(f"connection established------------ from {address}")


def receive_messages():
    while True:
        try:
            data = client.recv(1024).decode()
            if data.lower() == "exit" or not data:
                print("Client disconnected.")
                break
            print(f"\nClient: {data}")
        except:
            break

def send_messages():
    while True:
        message = input("You: ")
        client.send(message.encode())
        if message.lower() == "exit":
   
            break





threading.Thread(target=receive_messages, daemon=True).start()
send_messages()

client.close()
server.close()
print("Server closed.")
