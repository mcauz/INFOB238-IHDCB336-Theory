import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as senderSocket:
    senderSocket.connect(('localhost', 80))

    senderSocket.send('Hello World !'.encode('utf-8'))
    data = senderSocket.recv(1024)
    print(f'Received {data.decode("utf-8")}')

    senderSocket.send(b'end')
