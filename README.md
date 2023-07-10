# Server_script
# server script
## performs a lot of backend functionality well optimized for speed

# client
This code is a client application that communicates with a server using SSL/TLS encryption.
It sends a query string to the server and receives a response indicating whether the string exists in the server's database.
The code also measures the execution time for different file sizes.

## prerequisite
To run this code, you need the following:

Python 3.x installed on your system.
The socket and ssl modules, which are standard libraries in Python.

## setup
Clone or download the code repository to your local machine.

Make sure you have the server module in the same directory as the client code.
The server module contains the server configuration needed for the client.

## running the code
Open a terminal or command prompt.

Navigate to the directory containing the client code.

Run the following command to execute the client code:
### python client.py --query "your_query_string"

Replace "your_query_string" with the string you want to search for in the server's database.

### Example: python client.py --query "19;0;21;16;0;17;3;0;"
![Screenshot](https://github.com/Mumin8/Server_script/blob/main/op.PNG)
