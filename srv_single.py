import argparse, time
from socket import *

cong = "vegas"
cong = bytes(cong, 'ascii')

def parse_command_line(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

def create_srv_socket(address):
    listener = socket(AF_INET, SOCK_STREAM)
    listener.setsockopt(IPPROTO_TCP, TCP_CONGESTION, cong)
    listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def accept_connections_forever(listener):
    for i in range(3):
    	sock, address = listener.accept()
    	print('Accepted connection from {}'.format(address))
    	handle_conversation(sock, address)

def handle_conversation(sock, address):
    try:
        handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()

def handle_request(sock):
	filename='4.jpg'
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		sock.sendall(l)
		l = f.read(1024)
	f.close()

if __name__ == '__main__':
    address = parse_command_line('simple single-threaded server')

    listener = create_srv_socket(address)
    accept_connections_forever(listener)
