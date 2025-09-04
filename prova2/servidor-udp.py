import socket

# Cria o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 12345))

print("Servidor UDP esperando mensagens na porta 12345...")

while True:
    data, addr = sock.recvfrom(1024)  # 1024 bytes
    print(f"Recebido de {addr}: {data.decode()}")
    resposta = f"Eco: {data.decode()}"
    sock.sendto(resposta.encode(), addr)
