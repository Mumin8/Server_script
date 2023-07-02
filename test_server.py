import os
import pytest
import server
import configparser
import signal
import threading
import time
import requests
import socket
from server import start_server
from client import search_string

PORT = 8000
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
stop_server_flag = threading.Event()


def test_find_path():

    '''
    test_find_path: this handles the find_path cases
    '''

    config = configparser.ConfigParser()
    path = server.find_path()

    assert isinstance(path, str), " the path should be a string"

    assert path is not None and path != "", "The path must exist"

    assert "DEFAULT" not in config or 'linuxpath' not in config['DEFAULT']


def test_start_server():
    '''
    test_start_server: this starts the server
    '''
    FILE_PATH = server.find_path()
    REREAD_ON_QUERY = True
    USE_SSL = {
            'ssl': True,
            'certfile': 'server.crt',
            'keyfile': 'server.key'
            }

    # Start the server in a separate thread
    server_thread = threading.Thread(
            target=start_server,
            args=(HOST, PORT, FILE_PATH, REREAD_ON_QUERY, USE_SSL))
    server_thread.start()

    # Wait for the server to start
    time.sleep(1)

    # Stop the server by setting the stop_server_flag
    stop_server_flag.set()

    # Stop the server
    server_thread.join(timeout=1)

    # Assert that the server thread has stopped
    assert server_thread.is_alive()
