import sys
import time
import socket
import threading
import traceback
from queue import Queue
from typing import Tuple

open_clients = {}
messages = Queue()
stop_event = threading.Event()

def recieve_msgs(conn:socket.socket, addr:Tuple[str,int]):
  while not stop_event.is_set():
    msg = conn.recv(1024)
    if not msg: continue 
    msg = msg.decode('utf-8')
    if msg == '[EXIT]':
      conn.close()
      del open_clients[addr]
      print(f"Client disconnected... ")
      print(f"open_clients = {open_clients}")
      stop_event.set()
    messages.put((conn, msg)) 

def broadcast_msg():
  while not stop_event.is_set():
    sender, msg = messages.get()
    for addr, client in open_clients.items():
      try:
        if client == sender: continue
        client.sendall(msg.encode('utf-8'))
      except (BrokenPipeError, ConnectionResetError):
        del open_clients[addr]
        client.close()
      except:
        print(f"error = {traceback.format_exc()}")

def main(server:socket.socket):
  while not stop_event.is_set():
    try: 
      conn, addr = server.accept()
      open_clients[addr] = conn
      print(f"open_clients = {open_clients}")
      threading.Thread(
        target=recieve_msgs,
        args=(conn,addr,),
        daemon=True
      ).start()
    except KeyboardInterrupt:
      if len(open_clients):
        print("cannot close server, clients exist")
      else:
        print(f"exiting because, open_clients = {open_clients}")
        stop_event.set()

if __name__ == "__main__":
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(('127.0.0.1', 5000))
  server.listen()
  print("server listening on 127.0.0.1:5000")
  threading.Thread(target=broadcast_msg, daemon=True).start()
  main(server)

