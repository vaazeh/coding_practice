import socket
import threading




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.20", 8081))



print("Connected to server. Type 'exit' to quit.")




def receive_messages():
    while True:
        try:
            data = client.recv(1024).decode()
            if data.lower() == "exit" or not data:
                print("Server disconnected.")
                break
            print(f"\nServer: {data}")
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
print("Disconnected.")
