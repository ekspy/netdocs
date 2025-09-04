#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1. Este programa obtém a carga da CPU e a memória RAM disponível
#    e envia para um servidor de monitoramento a cada 3 segundos.
# 2. O programa usa sockets TCP que ficam conectados de forma
#    persistente com cada cliente
# 3. Usa a biblioteca psutil
#    Caso ela não esteja instalada no sistema, execute no Ubuntu:
#       sudo apt-get install gcc python3-dev
#       sudo pip3 install psutil
# 4. Caso ocorra erros ao obter as informações, envia -1 ao servidor
# 5. O cliente envia mensagens de tamanho fixo (30 bytes) contendo:
#      - o nome da maquina (hostname)
#      - a carga da CPU
#      - a memória disponível

import socket, time, sys, re
import argparse

try:
    import psutil
except:
    print('O modulo psutil não está instalado')
    
def monta_mensagem():
    print('Obtendo a carga de CPU e a memória disponível ...')
    hostname = socket.gethostname()
    try:
        uso_cpu = psutil.cpu_percent(interval=1.0)
        m = psutil.virtual_memory()
        mem_livre = m.available * 100 / m.total
    except:
        print('Erro ao obter as informações do sistema. Enviando valores -1 para o servidor')
        uso_cpu = -1.0
        mem_livre = -1.0
    mensagem = 'Hostname:{:10} Carga de CPU:{:5.1f}% Memória Disponível:{:5.1f}%'.format(hostname, uso_cpu, mem_livre)
    return mensagem

def cliente(server, ipv4):
    try:
        if ipv4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    except socket.error:
        print('Erro ao criar o socket.')
        sys.exit(1)

    if not server:
        if ipv4:
            server = '127.0.0.1'
        else:
            server = '::1'
    port = 5050                
    messageLen = 67

    # conecta com o servidor
    try:
        sock.connect((server, port))
    except socket.gaierror:
        print('Verifique o endereço do servidor.')
        sys.exit(1)
    except socket.error:
        print('Erro de conexão')
        sys.exit(1)

    while True:
        mensagem = monta_mensagem()
        print(mensagem)

        # envia a mensagem para o servidor
        try:
            sock.sendall(mensagem.encode())  # envia pelo socket
        except socket.error as e:
            print('Erro ao enviar os dados. Verifique a conexão: {}'.format(e))
            sock.close()
            sys.exit(1)

        # aguarda 3 segundos
        time.sleep(3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ipv4', action='store_true')
    parser.add_argument('--server', action='store')
    args = parser.parse_args()
    print(args.server)
    
    cliente(args.server, args.ipv4)
