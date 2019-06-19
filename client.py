import argparse, time
from socket import *

cong = "cubic"
cong = bytes(cong, "ascii")

def client(address, cause_error=False):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(IPPROTO_TCP, TCP_CONGESTION, cong)
    sock.connect(address)
    start = time.time()
    with open('videos/m.mkv', 'wb') as f:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            f.write(data)
    end = time.time()
    print(end - start)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)
