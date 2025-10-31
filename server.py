from typing import Tuple
import time
import socket
import threading
import traceback
from queue import Queue

open_clients = {}
messages = Queue()

def recieve_msgs(conn:socket.socket, addr:Tuple[str,int]):
  while True:
    try:
      msg = conn.recv(1024).decode('utf-8')
      if msg == '[EXIT]':
        conn.close()
        del open_clients[addr]
        print(f"Client disconnected open_clients = {open_clients}")
        break
      messages.put((conn, msg))
    except:
      print(f"error occured = {traceback.format_exc()}")
  return 

def broadcast_msg():
  while True:
    try: 
      sender, msg = messages.get()
      for addr, client in open_clients.items():
        if client != sender:
          client.sendall(msg.encode('utf-8'))
    except:
      print(f"error = {traceback.format_exc()}")
      break
  return

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5000))
server.listen()

if __name__ == "__main__":
  print("server listening on 127.0.0.1:5000")
  threading.Thread(target=broadcast_msg, daemon=True).start()
  while True:
    conn, addr = server.accept()
    open_clients[addr] = conn
    print(f"open_clients = {open_clients}")
    threading.Thread(
      target=recieve_msgs, args=(conn,addr,), daemon=True
    ).start() 

