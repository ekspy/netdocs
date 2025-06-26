#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1. Este servidor TCP recebe os dados de monitoramento dos clientes
# 2. O comando não bloqueante 'select' é usado para atender
#    vários clientes concorrentemente
# 3. As mensagens do cliente para o servidor têm tamnha fixo de 30 bytes


import socket, select, time, sys

def main():
    addr = ("", 5050) # escuta em todas as interfaces, porta 5050

    try:
        if socket.has_dualstack_ipv6():
            acceptSocket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
        else:
            acceptSocket = socket.create_server(addr)
    except socket.error as e:
        print('Erro ao criar o socket: {}'.format(e))
        sys.exit(1)

    messageLen = 67
    numClientes = 0
    readSockets = [acceptSocket]

    while True:
        try:
            rlist, wlist, elist = select.select(readSockets, [], [], 2)
        except select.error:
            print('Erro ao manipular os sockets com select.')
            sys.exit(1)
        if [rlist, wlist, elist] == [ [], [], [] ]:
            print('Fazendo qualquer processamento\n')
            pass
        else:
            for sock in rlist:
                if sock is acceptSocket:
                    # evento do acceptSocket
                    try:
                        dataSocket, addr = acceptSocket.accept()
                    except socket.error:
                        print('Erro ao aceitar conexão.')
                        sys.exit(1)
                    numClientes += 1
                    print('Conexao {} com {}'.format(numClientes, str(addr)))
                    # inclui o novo dataSocket na lista de readSockets
                    readSockets.append(dataSocket)
                else:
                    # evento em um dataSocket
                    print('Recebendo dados de {}'.format(sock.getpeername()))
                    chunks = []
                    count = 0
                    while count != messageLen:
                        try:
                            data = sock.recv(messageLen-count)
                        except socket.error:
                            print('Erro ao receber dados.')
                        if not data:
                            print('Fechando o socket.')
                            sock.close()
                            readSockets.remove(sock)
                            break
                        chunks.append(data.decode('utf-8'))
                        count += len(data)
                    print(''.join(chunks)+'\n')

if __name__ == "__main__":
    main()
