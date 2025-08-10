import socket



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.20", 7000))



while True:
    data = input()
    try:
      client.send(data.encode())
    except:
       client.close()
       
       break

print("disconnect")
