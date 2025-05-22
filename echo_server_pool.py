import socket
import threading
import queue

HOST = 'localhost'
PORT = 12345
NUM_THREADS = 10

# Fila de conexões
fila_conexoes = queue.Queue()

# Lista para controle das threads (True = ocupada, False = livre)
threads_ocupadas = [False] * NUM_THREADS
threads_lock = threading.Lock()

# Função executada por cada thread do pool
def trabalhador(thread_id):
    while True:
        conn, addr = fila_conexoes.get()  # Espera uma conexão da fila
        with threads_lock:
            threads_ocupadas[thread_id] = True  # Marca thread como ocupada

        print(f"[THREAD {thread_id}] Atendendo {addr}")
        try:
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"[{addr}] {data.decode()}")
                    conn.sendall(data)  # Echo
        except Exception as e:
            print(f"[THREAD {thread_id}] Erro: {e}")
        finally:
            with threads_lock:
                threads_ocupadas[thread_id] = False  # Marca como livre
            print(f"[THREAD {thread_id}] Finalizou atendimento de {addr}")

# Inicia o pool de threads
for i in range(NUM_THREADS):
    t = threading.Thread(target=trabalhador, args=(i,), daemon=True)
    t.start()

# Inicia o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escutando em {HOST}:{PORT} com {NUM_THREADS} threads fixas...")

    while True:
        conn, addr = server_socket.accept()
        print("Server_Socket accept")
        
        # Verifica se há alguma thread livre
        with threads_lock:
            if False in threads_ocupadas:
                print("False in threads_ocupadas")
                fila_conexoes.put((conn, addr))  # Envia a conexão para a fila
                msg = "Opa.\n"  #É pra não da erro NAO TIRA
                conn.sendall(msg.encode())
            else:
                # Todas ocupadas: envia aviso e desconecta
                print("Else")
                msg = "Servidor cheio. Tente novamente mais tarde.\n"
                conn.sendall(msg.encode())
                conn.close()
                print(f"[CHEIO] Rejeitada conexão de {addr}")
