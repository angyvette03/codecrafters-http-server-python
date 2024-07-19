# Uncomment this to pass the first stage
import socket
import threading
import os
import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    def parse_request(request):
        lines = request.split("\r\n")
        method, path, version = lines[0].split(" ")
        return method, path, version
    
    def response(path, request):
        resType = 'text/plain'
        if (path =='/'):
            return "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif ('user-agent' in path):
            lines = request.split("\r\n")
            userAgent = lines[2].split(": ")[1]
            length = str(len(userAgent))
            return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Length: {length}\r\n\r\n{userAgent}").encode()
        elif ("echo" in path):
            res = path.split('/')[2]
            length = str(len(res))
            body = str(res)
            return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Length: {length}\r\n\r\n{body}").encode()
        elif (path.startswith('/files')):
            directory = sys.argv[2]
            filename = path[7:]
            filePath = directory + filename
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                    return (f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}").encode()
            except Exception as e:
                    return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
        # else:
        #     return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen() 

    def handle_client_connection(client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {request}")
        
        # Parsing the request to get method, path, and version
        method, path, version = parse_request(request)
        
        # Generating the appropriate response based on the path
        http_response = response(path, request)
        
        # Sending the response back to the client
        client_socket.sendall(http_response)
        client_socket.close()
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()
        
if __name__ == "__main__":
    main()
