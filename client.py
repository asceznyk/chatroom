import time
import socket
import threading

def recieve_msgs(client:socket.socket):
  while True:
    try:
      msg = client.recv(1024).decode('utf-8')
      if msg == '[EXIT]':
        client.close()
        break
      print(f"other: {msg}")
    except:
      pass
  return

def send_msg(client:socket.socket):
  while True:
    msg = input("")
    client.sendall(msg.encode('utf-8'))
    if msg == '[EXIT]':
      break
  client.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))
threading.Thread(
  target=recieve_msgs,
  args=(client,),
  daemon=True
).start()

if __name__ == "__main__":
  print(f"client connected to server {client}")
  send_msg(client)


