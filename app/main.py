# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    def parse_request(request):
        lines = request.split("\r\n")
        method, path, version = lines[0].split(" ")
        splitPath = path.split("/")
        if len(splitPath) > 2:
            res = splitPath[2]
        else:
            res = ""
        return method, path, version, res
    
    def response(res):
        resType = 'text/plain'
        length = str(len(res))
        body = str(res)
        return (f"HTTP/1.1 200 OK\r\nContent-Type: {resType}\r\nContent-Length: {length}\r\n\r\n{body}").encode()
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen() 
    
    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024).decode()
        method, path, version, res = parse_request(data)
    
        http_response = response(res)
        client_socket.sendall(http_response)
        client_socket.close()
        

if __name__ == "__main__":
    main()
