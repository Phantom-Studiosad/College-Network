import socket
import threading
import pandas as pd

HEADER = 64
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
df = pd.read_csv('student.csv')


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    def cgpa(df, id):
        st = " "
        for i in range(len(df)):
            if df.loc[i, 'id'] == id:
                st = 'Roll no: ' + str(df.loc[i, 'id']) + '| Name: ' + str(df.loc[i, 'name']) + '| CGPA: ' + str(
                    df.loc[i, 'marks'])
                break
        return st

    def fees(df, id):

        for i in range(len(df)):
            if df.loc[i, 'id'] == id and df.loc[i, 'fees_paid'] == True:
                return 'Fees Paid'
        return 'Fees due'

    def attendance(df, id):
        st = " "
        for i in range(len(df)):
            if df.loc[i, 'id'] == id:
                st = ' Roll no: ' + str(df.loc[i, 'id']) + '| Name: ' + str(df.loc[i, 'name']) + '| Attendance: ' + str(
                    df.loc[i, 'attendance'])
                break
        return st

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg[0] == 'C':
                split_data = msg.split()
                pts = cgpa(df, int(split_data[1]))
                print(f"[{addr}] {msg}")
                conn.send(pts.encode(FORMAT))

            elif msg[0] == 'A':
                split_data = msg.split()
                attnd = attendance(df, int(split_data[1]))
                print(f"[{addr}] {msg}")
                conn.send(attnd.encode(FORMAT))
            elif msg[0] == 'F':
                split_data = msg.split()
                fee = fees(df, int(split_data[1]))
                print(f"[{addr}] {msg}")
                conn.send(fee.encode(FORMAT))
            else:
                print(f"[{addr}] {msg}")
                conn.send('Command incorrect'.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
