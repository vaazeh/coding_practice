import socket
import threading
import datetime

file_name = f"chat_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.1.20", 8081))
server.listen()
print("waiting for connection-----------")

client, address = server.accept()
print(f"connection established------------ from {address}")

def save_chat(sender, message):
    with open(file_name, "a") as f:
        f.write(f"{sender}: {message}\n")

def receive_messages():
    while True:
        try:
            data = client.recv(1024).decode()
            if data.lower() == "exit" or not data:
                print("Client disconnected.")
                save_chat("SYSTEM", "Client disconnected.")
                break
            print(f"\nClient: {data}")
            save_chat("Client", data)
        except:
            break

def send_messages():
    while True:
        message = input("You: ")
        client.send(message.encode())
        save_chat("Server", message)
        if message.lower() == "exit":
            save_chat("SYSTEM", "Server closed chat.")
            break

threading.Thread(target=receive_messages, daemon=True).start()
send_messages()

client.close()
server.close()
print("Server closed.")
save_chat("SYSTEM", "Server closed.")
