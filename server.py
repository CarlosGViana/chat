import socket
import threading
import sqlite3



HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


clients = []
nicknames = []

def passar(mensagem):
    for client in clients:
        client.send(mensagem)

    
def handle(client):
    while True:
        try:
            mensagem = client.recv(1024)
            mensagem = mensagem.decode('utf-8')

            palavra = []
            banco = sqlite3.connect('banco_palavras.db') 
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS palavras (palavra text)")

            cursor.execute("SELECT * FROM palavras")
            for linha in cursor.fetchall():
                palavra.append(linha[0])

            for x in palavra:
                mensagem = mensagem.replace(x, '****')
            print( f"{mensagem}")

            mensagem = mensagem.encode('utf-8')
            passar(mensagem)
        except:
            index = clients.index(clients)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)
        print(f"O nome do Usuário é {nickname.decode('utf-8')}")
        passar(f"{nickname.decode('utf-8')} entrou no chat!\n".encode('utf-8'))
        

        
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()
        
print("Servidor rodando...")
receive()
    
