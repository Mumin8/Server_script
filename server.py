#!/usr/bin/env python

import socket
import threading


def find_path() -> str:

    with open('config.config', 'r') as conf_file:
        for line in conf_file:
            if line.startswith('linuxpath='):
                file_path = line
                print(f' this is the path {file_path}')
                break
            else:
                ValueError('path not in configuration file')
    return file_path


def handle_client(client_socket: object, file_path: str):
    '''
    handle_client: it handles the client clear text string

    args:
        client_socket: the object of the client socket
        file_path: the path to the file
    '''

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # decode the received string from the client
        the_string = data.decode('utf-8')

        with open(file_path.lstrip('linuxpath=/').rstrip('\n'), 'r') as file:
            for line in file:
                if line.strip() == the_string:
                    resp = b"STRING EXISTS"
                    client_socket.send(resp)
                    break
            else:
                resp = b'STRING DOES NOT EXIST'
                client_socket.send(resp)

    # Close the client socket
    client_socket.close()


def start_server(host: str, port: int, file_path: str):
    '''
    start_server: binds a port and responds to unlimited amount of
    concurrent connections

    args:
        host: a string representing the host or ip address of the server
        port: an integer representing the port number of the server to bind
    '''

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host} : {port}")

    while True:
        # Accept a client connection
        client_sock, client_addr = server_socket.accept()
        print(f"New connection from {client_addr[0]} : {client_addr[1]}")

        # Start a new thread to handle the client
        client_th = threading.Thread(
                    target=handle_client,
                    args=(client_sock, file_path,))
        client_th.start()


if __name__ == '__main__':
    # Specify the host and port to bind the server to
    HOST = '127.0.0.1'
    PORT = 8000
    # Start the server
    file_path = find_path()
    start_server(HOST, PORT, file_path)
