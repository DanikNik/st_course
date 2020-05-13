#!/usr/bin/env python3
import logging
import queue
import sys
import threading

from client.client import Client

from ui.mainwindow import main

#
# def reading_func(c: Client):
#     while True:
#         frame = c.read()
#         if frame.frametype == frame.TYPE_DATA:
#             print(f"[{frame.src}] {frame.data}")
#
#
# def read_kbd_input(in_queue):
#     while True:
#         try:
#             in_queue.put(input())
#         except KeyboardInterrupt:
#             sys.exit(0)
#
#
# def main_f():
#     # com1 = sys.argv[1]
#     # com2 = sys.argv[2]
#     # address = int(sys.argv[3])
#     com1 = input("COM1: ")
#     com2 = input("COM2: ")
#     address = int(input("ADDR: "))
#     print(f"COM PORTS ARE {com1} and {com2}")
#     print(f"ADDRESS IS {address}")
#
#     input_queue = queue.Queue()
#     input_thread = threading.Thread(
#         target=read_kbd_input, args=(input_queue,), daemon=True
#     )
#     input_thread.start()
#     client = Client(address, com1, com2)
#     client.start()
#     reader = threading.Thread(target=reading_func, args=[client])
#     try:
#         reader.start()
#         while True:
#             if input_queue.qsize() > 0:
#                 input_str: str = input_queue.get()
#                 if input_str == "OPEN":
#                     client.register()
#                     continue
#                 elif input_str == "CLOSE":
#                     for conn in client.connections:
#                         conn.close()
#                     continue
#                 dst, data = input_str.split(" ", 1)
#                 dst = int(dst)
#                 print(f"SENDING {data} to {dst}")
#                 client.send(data, dst)
#     except Exception as e:
#         logging.exception("EXCEPTION OCCURED")
#
#         client.close()
#         reader.join()


if __name__ == "__main__":
    main()
