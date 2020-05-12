#!/usr/bin/env python
import queue
import sys
import threading

from client.client import Client


def reading_func(c: Client):
    while True:
        frame = c.read()
        if frame.frametype == frame.TYPE_DATA:
            print(f'[{threading.get_ident()}] CAPTURED: {frame.data}')


def read_kbd_input(input_queue):
    while True:
        try:
            # Receive keyboard input from user.
            input_str = input()

            # Enqueue this input string.
            # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them
            # which would otherwise need to be treated as one atomic operation.
            input_queue.put(input_str)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':

    input_queue = queue.Queue()

    # Create & start a thread to read keyboard inputs.
    # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. This is desired since
    # this thread has no cleanup to do, which would otherwise require a more graceful approach to clean up then exit.
    input_thread = threading.Thread(target=read_kbd_input, args=(input_queue,), daemon=True)
    input_thread.start()

    com1 = sys.argv[1]
    com2 = sys.argv[2]
    address = int(sys.argv[3])
    print(f'COM PORTS ARE {com1} and {com2}')
    print(f'ADDRESS IS {address}')
    client = Client(address, com1, com2)
    client.run()
    reader = threading.Thread(target=reading_func, args=[client])
    try:
        reader.start()
        while True:
            if input_queue.qsize() > 0:
                input_str = input_queue.get()
                if input_str == 'OPEN':
                    client.register()
                    continue
                elif input_str == 'CLOSE':
                    for conn in client.connections:
                        conn.close()
                    continue
                dst, data = input_str.split(' ')
                dst = int(dst)
                print(f'SENDING {data} to {dst}')
                client.send(data, dst)
    except:
        client.stop()
        reader.join()
