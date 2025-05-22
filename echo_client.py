import socket  # Importa a biblioteca de sockets para comunicação em rede

HOST = 'localhost'  # Endereço IP do servidor (deve ser o mesmo do servidor)
PORT = 12345        # Porta usada pelo servidor

# Cria um socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Conecta-se ao servidor no endereço e porta especificados
    client_socket.connect((HOST, PORT))
    print("Conectado ao servidor!")

    # Loop principal para enviar mensagens ao servidor
    while True:
        # Solicita ao usuário que digite uma mensagem
        msg = input("Digite uma mensagem (ou 'sair'): ")

        # Se o usuário digitar 'sair', encerra o loop
        if msg.lower() == 'sair':
            break

        # Envia a mensagem codificada como bytes para o servidor
        client_socket.sendall(msg.encode())

        # Aguarda a resposta do servidor (echo)
        resposta = client_socket.recv(1024)

        # Exibe a resposta recebida do servidor
        print(f"Echo do servidor: {resposta.decode()}")
