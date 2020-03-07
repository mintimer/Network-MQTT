import socket, sys, os
from threading import Thread

def closeAllConnect ():
    for topic in portlist:
        for socket in portlist[topic]:
            message = b'CLOSE_CONNECT'
            socket['socket_connection'].send(message)

def closeConnect(client_address):
    for topic in portlist:
        for i in range(len(portlist[topic])):
            if portlist[topic][i]['client_address'] == client_address:
                print('Closing Connection from {}'.format(client_address) + ' topic "%s"' % topic)
                del portlist[topic][i]

def publishData(topic,data):
    for anytopic in portlist:
        if anytopic == topic:
            for socket in portlist[topic]:
                socket['socket_connection'].send(data.encode())

def isSubcriber(message):
    return 'SUB\t' in message

def isPublisher(message):
    return 'PUB\t' in message

def manage_connect(socket_connection, client_address, sock):
    print('connection from', client_address)
    while True:
        try:
            message = socket_connection.recv(2000)
            message = message.decode('utf-8')
            if message:
                if isSubcriber(message):
                    splited = str(message).split('\t')
                    topic = splited[1]
                    if topic == 'END_CONNECT':
                        closeConnect(client_address)
                        break
                    else :
                        print('received from Subscriber topic "%s"' % topic)
                        if topic in portlist:
                            portlist[topic].append({'socket_connection':socket_connection , 'client_address':client_address })
                        else :
                            portlist[topic] = [{'socket_connection':socket_connection , 'client_address':client_address }]
                if isPublisher(message):
                    splited = str(message).split('\t')
                    topic = splited[1]
                    data = splited[2]
                    publishData(topic,data)
        except BlockingIOError:
            pass

def main():

    server_address = (str(sys.argv[1]),20000)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connectionskey
    sock.listen(1)
    sock.setblocking(0)
    while True:
        try:
            socket_connection, client_address = sock.accept()
            try:
                Thread(target=manage_connect,args=(socket_connection,client_address,sock)).start()
            except:
                print("Cannot start thread..")
        except BlockingIOError:
            pass

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        portlist = dict()
        main()
    except KeyboardInterrupt:
        closeAllConnect()
        print('sending connect closing message to all client')
        try:
            sock.close()
            sys.exit(0)
        except:
            os._exit(0)