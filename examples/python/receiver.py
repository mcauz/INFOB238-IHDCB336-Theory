import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiverSocket:
    receiverSocket.bind(('', 80))
    receiverSocket.listen()
    print('Waiting for a connection')

    (senderSocket, address) = receiverSocket.accept()
    print(f'Accepted connection from {address}')

    with senderSocket:
        while True:
            data = senderSocket.recv(1024)
            if data == b'end':
                break
            print(f'Received {data.decode('utf-8')}')
            senderSocket.sendall(data)
