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
        responses = {
            '/': "HTTP/1.1 200 OK\r\n\r\n"
        }
        
        default_response = "HTTP/1.1 404 Not Found\r\n\r\n"
        
        responses.get(path, default_response)
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen() 
    
    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024)
        method, path, version = parse_request(data)
        http_response = response(path)
        client_socket.sendall(http_response.encode())
        client_socket.close()
        
        
    
    


if __name__ == "__main__":
    main()
