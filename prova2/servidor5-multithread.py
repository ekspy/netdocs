#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# 1. Este servidor TCP recebe os dados de monitoramente dos clientes
# 2. Ao invés de select (não bloqueante) utiliza uma thread para cada cliente
#    Para essa aplicação, select é mais eficiente
#    O objetivo do exemplo é demonstrar o uso de threads
# 3. As mensagens do cliente para o servidor têm tamnha fixo de 30 bytes

import socket, select, time, sys, threading

messageLen = 67

def handle_client(dataSocket, addr):
    global messageLen
    while True:
        chunks = []
        count = 0
        while count != messageLen:
            try:
                data = dataSocket.recv(messageLen-count)
            except socket.error:
                print('Erro ao receber dados.')
            if not data:
                print('Fechando o socket.')
                dataSocket.close()
                return
            chunks.append(data.decode('utf-8'))
            count += len(data)
        print('Mensage recebida de {}'.format(dataSocket.getpeername()))    
        print(''.join(chunks))

def main():
    global messageLen
    addr = ("", 5050)  # escuta em todas as interfaces, porta tcp/5050
    print('Iniciando o monitor de temperatura. Aguardando clientes.')
    try:
        if socket.has_dualstack_ipv6():
            acceptSocket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
        else:
            acceptSocket = socket.create_server(addr)
    except socket.error as e:
        print('Erro ao criar o socket: {}'.format(e))
        sys.exit(1)

    numClientes = 0

    while True:
        try:
            dataSocket, addr = acceptSocket.accept()
        except socket.error:
            print('Erro ao aceitar conexão.')
            sys.exit(1)
        numClientes += 1
        print('Conexao {} com {}'.format(numClientes, str(addr)))
        # iniciando nova thread
        thread = threading.Thread(target=handle_client, args=(dataSocket, addr))
        thread.start()

if __name__ == "__main__":
    main()

# obs: para não bloquear a thread principal no accept(),
#      use select() como no exemplo server4.py
