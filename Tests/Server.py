import socket


TCP_IP = '192.168.168.109'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
    try:
        data = conn.recv(BUFFER_SIZE)
        if data:
            conn.send(data)  # echo
            decoded = data.decode()
            print("received data:", decoded)
    except ConnectionResetError:
        print("Connection closed: Goodbye")
conn.close()