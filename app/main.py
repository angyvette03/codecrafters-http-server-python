# Uncomment this to pass the first stage
import socket
import threading
import sys
import gzip

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    def parse_request(request):
        lines = request.split("\r\n")
        method, path, version = lines[0].split(" ")
        return method, path, version
    
    def response(method, path, request):
        resType = 'text/plain'
        if method == 'GET':
            if (path =='/'):
                return "HTTP/1.1 200 OK\r\n\r\n".encode()
            elif ('user-agent' in path):
                lines = request.split("\r\n")
                userAgent = lines[2].split(": ")[1]
                length = str(len(userAgent))
                return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Length: {length}\r\n\r\n{userAgent}").encode()
            elif ("echo" in path):
                acceptEncodingHeader = request.split("\r\n")[2]
                # print("encoding headers", acceptEncodingHeader)
                
                if ('gzip' in acceptEncodingHeader):
                #     return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Encoding: gzip\r\n\r\n").encode()
                # else:
                    res = path.split('/')[2]
                    compressedBody = gzip.compress(res.encode())
                    length = str(len(compressedBody))
                    response = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Encoding: gzip\r\n"
                        f"Content-Type: {resType}\r\n"
                        f"Content-Length: {length}\r\n"
                        f"\r\n"
                    ).encode() + compressedBody
                    return response
                elif(acceptEncodingHeader == 'invalid-encoding'):
                # else:
                    return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\n\r\n{len(path.split('/')[2])}").encode()
                else:
                    return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\n\r\n{len(path.split('/')[2])}").encode()
            elif (path.startswith('/files')):
                directory = sys.argv[2]
                filename = path[7:]
                try:
                    with open(f"/{directory}/{filename}", "r") as f:
                        body = f.read()
                        return (f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}").encode()
                except Exception as e:
                        return f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else: 
                return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif (method == 'POST'):
            if (path.startswith('/files')):
                directory = sys.argv[2]
                filename = path[7:]
                reqBody = request.split("\r\n")[-1]
                try:
                    with open(f"{directory}/{filename}", "w") as f:
                        f.write(reqBody)
                    return f"HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    return f"HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen() 

    def handle_client_connection(client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        # print(f"Received: {request}")
        
        # Parsing the request to get method, path, and version
        method, path, version = parse_request(request)
        print(f"Method: {method}")
        print(f"Path: {path}")
        
        # Generating the appropriate response based on the path
        http_response = response(method, path, request)
        print(f"Request: {request}")
        # print(f"Response: {http_response.decode()}")
        
        
        # Sending the response back to the client
        client_socket.sendall(http_response)
        client_socket.close()
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()
        
if __name__ == "__main__":
    main()
