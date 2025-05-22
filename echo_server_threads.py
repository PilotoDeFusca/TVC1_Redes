import socket
import threading  # Para lidar com múltiplos clientes simultaneamente

HOST = 'localhost'
PORT = 12345

# Função que será executada por cada thread para tratar um cliente
def lidar_com_cliente(conn, addr):
    print(f"[NOVA CONEXÃO] Cliente conectado: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[DESCONECTADO] Cliente {addr} saiu.")
                break
            print(f"[{addr}] Recebido: {data.decode()}")
            conn.sendall(data)  # Envia o mesmo dado de volta (echo)

# Cria o socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escutando em {HOST}:{PORT}...")

    while True:
        # Aceita conexões de clientes
        conn, addr = server_socket.accept()

        # Cria uma nova thread para lidar com o cliente
        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
        thread.start()

        print(f"[ATIVO] Threads em execução: {threading.active_count() - 1}")
