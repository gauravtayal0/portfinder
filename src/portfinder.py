import argparse
import os
import random
import socket
import sys

# The legacy Bind, IsPortFree, etc. names are not exported.
__all__ = ('bind', 'is_port_free', 'pick_unused_port')

_PROTOS = [(socket.SOCK_STREAM, socket.IPPROTO_TCP),
           (socket.SOCK_DGRAM, socket.IPPROTO_UDP)]


def bind(port, socket_type, socket_proto):
    got_socket = False
    for family in (socket.AF_INET6, socket.AF_INET):
        try:
            sock = socket.socket(family, socket_type, socket_proto)
            got_socket = True
        except socket.error:
            continue
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))
            if socket_type == socket.SOCK_STREAM:
                sock.listen(1)
            port = sock.getsockname()[1]
        except socket.error:
            return None
        finally:
            sock.close()
    return port if got_socket else None

Bind = bind


def is_port_free(port):
    return bind(port, *_PROTOS[0]) and bind(port, *_PROTOS[1])

IsPortFree = is_port_free


def pick_unused_port(low=15000, high=25000):
    port = None
    return _pick_unused_port(low, high)

PickUnusedPort = pick_unused_port


def _pick_unused_port(low, high):

    rng = random.Random()
    for _ in range(10):
        port = int(rng.randrange(low, high))
        if is_port_free(port):
            return port

    
    while True:
        port = bind(0, _PROTOS[0][0], _PROTOS[0][1])
        if port and bind(port, _PROTOS[1][0], _PROTOS[1][1]):
            return port


def main():

    parser = argparse.ArgumentParser(description='port finder app')
    parser.add_argument("-low", type=int, default=15000, help='lower range port')
    parser.add_argument("-high", type=int, default=25000, help='higher range port')
    args = parser.parse_args()

    port = pick_unused_port(args.low, args.high)
    if not port:
        sys.exit(1)
    print port


if __name__ == '__main__':
    main()