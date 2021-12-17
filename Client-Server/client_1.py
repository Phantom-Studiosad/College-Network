import socket

HEADER = 64
PORT = 5052
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.6"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def main():
    print("\n[SERVER] Connected.")
    while 1:

        inp = input("""---------------------------------------------------

                  1.[C] View CGPA
                  2.[A] View Attendance
                  3.[F] View fee status
                  4.[E] Exit

                  Please select the operation of your choice : """)
        if inp == 'E':
            send(DISCONNECT_MESSAGE)
            break
        else:
            send(inp)

    print("\n[SERVER] Disconnected.")


main()


