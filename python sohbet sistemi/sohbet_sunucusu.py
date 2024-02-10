import socket
import threading

# Sunucu ayarları
HOST = 'localhost'
PORT = 5050

# Yeni istemci işleme fonksiyonu
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} bağlandı.")

    connected = True
    while connected:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"[{addr}] {message}")

                # Diğer istemcilere iletiliyor
                broadcast(message)
            else:
                break
        except Exception as e:
            print(f"Hata: {e}")
            break

    print(f"[DISCONNECTED] {addr} bağlantı kesildi.")
    conn.close()

# İstemcilere mesaj ileten fonksiyon
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Hata: {e}")
            client.close()
            remove_client(client)

# Bağlı istemci listesinden istemciyi kaldıran fonksiyon
def remove_client(client):
    if client in clients:
        clients.remove(client)

# Ana işlev
def start_server():
    server.listen()
    print(f"[LISTENING] Sunucu {HOST}:{PORT} adresinde dinliyor...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        clients.append(conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Sunucuyu başlat
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []

print("[STARTING] Sunucu başlatılıyor...")
start_server()
