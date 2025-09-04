import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

servidor = ('localhost', 12345)

while True:
    mensagem = input("Digite uma mensagem (ou 'sair'): ")
    if mensagem == 'sair':
        break
    sock.sendto(mensagem.encode(), servidor)
    resposta, _ = sock.recvfrom(1024)
    print("Resposta do servidor:", resposta.decode())
