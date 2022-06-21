import socket

URLS = {
    '/': 'hello index',
    '/blog': 'hello blog'

}

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_headers(method, url):
    if method != 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 405)
    return ('HTTP/1.1 200 Ok\n\n', 200)


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    return (headers + 'Hello').encode()



def run():
    # AF_INET - IPv4
    # SOCK_STREAM - TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # связываем субъекта с конкретным адресом и портом
    server_socket.bind(('localhost', 5001))

    # указание на то чтобы сокет начал прослушивать свой порт
    server_socket.listen()

    while True:
        # получение ответа серверным сокетом
        client_socket, addr = server_socket.accept()

        # запрос клиента
        request = client_socket.recv(1024)
        print(request)
        print(addr)

        response = generate_response(request.decode('utf-8'))

        # ответ клиенту
        client_socket.sendall(response)
        client_socket.close()

if __name__ == '__main__':
    run()