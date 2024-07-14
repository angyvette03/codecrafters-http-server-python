# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    def parse_request(request):
        lines = request.split("\r\n")
        method, path, version = lines[0].split(" ")
        return method, path, version
    
    def response(path):
        if (path[1]=='/'):
            return "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif ("echo" in path):
            resType = 'text/plain'
            res = path.split('/')[2]
            length = str(len(res))
            body = str(res)
            return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Length: {length}\r\n\r\n{body}").encode()
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen() 
    
    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode()
        method, path, version = parse_request(data)
        http_response = response(path)
        client_socket.sendall(http_response)
        client_socket.close()
if __name__ == "__main__":
    main()
