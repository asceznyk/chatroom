import time
import socket
import threading
import traceback
import sys
from contextlib import suppress

def recieve_msgs(client:socket.socket):
  while not stop_event.is_set():
    try:
      msg = client.recv(1024).decode('utf-8')
      if msg == '[EXIT]': continue
      print(f"other: {msg}")
    except:
      print(f"error = {traceback.format_exc()}")
      stop_event.set()
  return

def send_msg(client:socket.socket):
  while not stop_event.is_set():
    try:
      msg = input()
      client.sendall(msg.encode('utf-8'))
      if msg == '[EXIT]':
        stop_event.set()
        break
      sys.stdout.write("\033[F")
      sys.stdout.write("\r\033[K")
      sys.stdout.flush()
      print(f"you: {msg}")
    except KeyboardInterrupt:
      print("exiting..")
      client.sendall("[EXIT]".encode('utf-8'))
      stop_event.set()
    except:
      print(f"Exception: {traceback.format_exc()}")
  return

if __name__ == "__main__":
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 5000))
  stop_event = threading.Event()
  print(f"client connected to server {client}")
  threading.Thread(
    target=recieve_msgs,
    args=(client,),
    daemon=True
  ).start()
  send_msg(client)


