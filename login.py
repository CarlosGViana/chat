from PyQt5 import  uic,QtWidgets
import sqlite3
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


HOST = '127.0.0.1'
PORT = 9090


def chama_segunda_tela():
    primeira_tela.label_4.setText("")
    nome_usuario = primeira_tela.lineEdit.text()
    senha = primeira_tela.lineEdit_2.text()
    banco = sqlite3.connect('banco_cadastro.db')    
    cursor = banco.cursor()
    try:
        cursor.execute("SELECT senha FROM cadastro WHERE login ='{}'".format(nome_usuario))
        senha_bd = cursor.fetchall()
        
        banco.close()
       
    except:
        print("Erro ao validar o login")
        primeira_tela.label_4.setText("Dados de login incorretos!")
        return chama_segunda_tela
       
    if senha == senha_bd[0][0]:
        primeira_tela.close()
        segunda_tela.show()
    else :
        primeira_tela.label_4.setText("Senha incorreta!")
    

def logout():
    segunda_tela.close()
    class Client:
    
            def __init__(self, host, port):
                
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((host, port))

                msg = tkinter.Tk()
                msg.withdraw()

                self.nickname = simpledialog.askstring("Usuário", "Digite um apelido:", parent = msg)


                self.gui_done = False
                self.running = True

                gui_thread = threading.Thread(target = self.gui_loop)
                receive_thread = threading.Thread(target = self.receive)

                gui_thread.start()
                receive_thread.start()

            def gui_loop(self):
                self.win = tkinter.Tk()
                self.win.configure(bg = "lightgray")
                self.win.title('Chat')

                self.chat_label = tkinter.Label(self. win, bg = "lightgray")
                self.chat_label.config(font=("Arial, 12"))
                self.chat_label.pack(padx = 20, pady = 5)

                self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
                self.text_area.pack(padx = 20, pady = 5)
                self.text_area.config(state = 'disable')

                self.msg_label = tkinter.Label(self. win, text = "Mensagem:", bg = "lightgray")
                self.msg_label.config(font=("Arial, 12"))
                self.msg_label.pack(padx = 20, pady = 5)

                self.input_area = tkinter.Text(self.win, height = 3)
                self.input_area.pack(padx = 20, pady = 5)

                self.send_button = tkinter.Button(self.win, text= "Enviar", command = self.write)
                self.send_button.config(font=("Arial, 12"))
                self.send_button.pack(padx = 20, pady = 5)

                self.gui_done = True

                self.win.protocol("WM_DELETE_WINDOW", self.stop)

                self.win.mainloop()

            def write(self):
                mensagem = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
                self.sock.send(mensagem.encode('utf-8'))
                self.input_area.delete('1.0', 'end')

            def stop(self):
                self.running = False
                self.win.destroy()
                self.sock.close()
                exit(0)

            def receive(self):
                while self.running:
                    try:
                        mensagem = self.sock.recv(1024).decode('utf-8')
                        if mensagem == 'NICK' :
                            self.sock.send(self.nickname.encode('utf-8'))
                        else:
                            if self.gui_done:
                                self.text_area.config(state = 'normal')
                                self.text_area.insert('end', mensagem)
                                self.text_area.yview('end')
                                self.text_area.config(state = 'disable')
                    except ConnectionAbortedError:
                        break
                    except:
                        print("Error")
                        self.sock.close()
                        self.stop()
                        break  

    client = Client(HOST, PORT)
    
   #primeira_tela.show()

def abre_tela_cadastro():
    tela_cadastro.show()


def cadastrar():
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    if (senha == c_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db') 
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)")
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+login+"','"+senha+"')")

            banco.commit() 
            banco.close()
            tela_cadastro.label.setText("Usuario cadastrado com sucesso")
            tela_cadastro.close()
            return chama_segunda_tela

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
    else:
        tela_cadastro.label.setText("As senhas digitadas estão diferentes")
    

    


app=QtWidgets.QApplication([])
primeira_tela=uic.loadUi("primeira_tela.ui")
segunda_tela = uic.loadUi("segunda_tela.ui")
tela_cadastro = uic.loadUi("tela_cadastro.ui")
primeira_tela.pushButton.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(logout)
primeira_tela.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
primeira_tela.pushButton_2.clicked.connect(abre_tela_cadastro)
tela_cadastro.pushButton.clicked.connect(cadastrar) 


primeira_tela.show()
app.exec()