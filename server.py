#!/usr/bin/env python

import configparser
import os
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from logging import basicConfig, DEBUG, debug, info
from threading import Thread
from time import time


def find_path() -> str:
    '''
    find_path: the function to find the path to the file


    Return:
            the path to the file

    '''
    try:
        # configparser object
        config = configparser.ConfigParser()
        config.read('config.config')

        if 'DEFAULT' in config:
            if 'linuxpath' in config['DEFAULT']:
                # obtain the exact path from the configuration file
                file_path = config['DEFAULT']['linuxpath']
                return file_path
        raise ValueError('path not in configuration file')

    except IOError:
        raise ValueError('Error reading configuration file')


def handle_client(
        client_socket: object, file_path: str, reread_on_query: bool):
    '''
    handle_client:
        it handles the client clear text string

    args:
        client_socket: the object of the client socket

        file_path:
            the path to the file to read from

        reread_on_query:
            the boolean to determine whether on not to read from the file again
    '''
    start = time()
    debug(f"Requesting IP: {client_socket.getpeername()[0]}")
    debug(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # decode the received string from the client and strip null characters
        the_string = data.decode('utf-8').strip('\x00')

        if reread_on_query:
            # checks whether the query string is in the file and read ones
            # file_content = read_file(file_path)
            with open(file_path.lstrip(
                    'linuxpath=/').rstrip('\n'), 'r') as file:
                if the_string in file.read():
                    resp = "STRING EXISTS\n"
                else:
                    resp = "STRING DOES NOT EXIST\n"
        else:
            # goes through the file to look for a match
            with open(file_path.lstrip('linuxpath=/').rstrip('\n'),
                      'r') as file:

                for line in file:
                    if line.strip() == the_string:
                        resp = "STRING EXISTS\n"
                        break
                else:
                    resp = 'STRING DOES NOT EXIST\n'

        debug(f"Search query: {the_string}")
        client_socket.send(resp.encode('utf-8'))
        execution_time = time() - start
        debug(f"Execution time: {execution_time*1000} miliseconds")

    # Close the client socket
    client_socket.close()


def start_server(host: str, port: int, file_path: str,
                 reread_on_query: bool, use_ssl: bool
                 ):
    '''
    start_server: binds a port and responds to unlimited amount of
    concurrent connections

    args:
        host:
            a string representing the host or ip address of the server
        port:
            an integer representing the port number of the server to bind
        file_path:
                the path to the file to read from
        reread_on_query:
                boolean to check whether to reread a file or not
        '''

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    if use_ssl:
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # Load server-side certificate and key
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        # Wrap the socket with SSL/TLS
        server_socket = context.wrap_socket(server_socket, server_side=True)
    

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(5)
    info(f"Server listening on {host} : {port}")

    # create threadpoolexecutor with 10 max_workers
    executor = ThreadPoolExecutor(max_workers=10)

    while True:
        # Accept a client connection
        client_sock, client_addr = server_socket.accept()
        info(f"New connection from {client_addr[0]} : {client_addr[1]}")

        # submit client handling task to the executor
        executor.submit(handle_client,
                        client_sock, file_path, reread_on_query)

        # Start a new thread to handle the client
        # client_th = Thread(
        # target=handle_client,
        # args=(client_sock, file_path, reread_on_query))

        # start the thread
        # client_th.start()


if __name__ == '__main__':

    # Linux daemon/service installation instructions
    if sys.platform.startswith('linux'):
        if os.geteuid() != 0:
            info("Please run the script as root to \
                    install it as a Linux service.")
            sys.exit(1)

        service_name = 'myserver'
        service_file = f'/etc/systemd/system/{service_name}.service'
        script_path = os.path.abspath(__file__)

        service_content = f"""
                                [Unit]
                                Description=My Server
                                After=network.target

                                [Service]
                                ExecStart={sys.executable} {script_path}
                                WorkingDirectory={os.path.dirname(script_path)}
                                Restart=always

                                [Install]
                                WantedBy=multi-user.target
                            """
        try:
            with open(service_file, 'w') as f:
                f.write(service_content)
                info(f"Created service file: {service_file}")
        except Exception as e:
            info(f"Failed to create service file: {str(e)}")
            sys.exit(1)

        os.system('systemctl daemon-reload')
        os.system(f"systemctl enable {service_name}")
        os.system(f"systemctl start {service_name}")
        info(f"Installed and started the service: {service_name}")

    # Specify the host and port to bind the server to
    HOST = '127.0.0.1'
    PORT = 8000

    REREAD_ON_QUERY = True

    # you can easily come here and turn ssl on and off
    USE_SSL = True

    # Start the server
    file_path = find_path()
    basicConfig(
            level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s'
            )
    start_server(HOST, PORT, file_path, REREAD_ON_QUERY, USE_SSL)
