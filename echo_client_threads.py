import socket

HOST = 'localhost'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))
        # print("Conectado ao servidor!")

        # Verifica se o servidor recusou por estar cheio
        resposta = client_socket.recv(1024).decode()
        
        if "Servidor cheio" in resposta:
            print("Resposta do servidor:", resposta)
        else:
            print("Conectado ao servidor!")
            # print("Servidor pronto para mensagens.")
            while True:
                msg = input("Digite uma mensagem (ou 'sair'): ")
                if msg.lower() == 'sair':
                    break

                client_socket.sendall(msg.encode())
                resposta = client_socket.recv(1024)
                print(f"Echo do servidor: {resposta.decode()}")
    except Exception as e:
        print("Erro ao conectar ou comunicar com o servidor:", e)
