import sys
from PyQt6.QtWidgets import *
import socket
import threading

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()
        widget = QWidget()
        self.setWindowTitle("Un serveur de chat")
        self.resize(500,350)
        self.setCentralWidget(widget)

        self.serveur_label = QLabel("Serveur")
        self.serveur_value = QLineEdit("")
        self.port_label = QLabel("Port")
        self.port_value = QLineEdit("")
        self.nbr_client_label = QLabel("Nombre de clients maximum")
        self.nbr_client_value = QLineEdit("")
        self.start_serv = QPushButton("Démarrage du serveur")
        self.result = QLineEdit("")
        self.result.setEnabled(False)
        self.quitter = QPushButton("Quitter")

        grid = QGridLayout()
        widget.setLayout(grid)
        grid.addWidget(self.serveur_label, 0, 0)
        grid.addWidget(self.serveur_value, 0, 1)
        grid.addWidget(self.port_label, 1, 0)
        grid.addWidget(self.port_value, 1, 1)
        grid.addWidget(self.nbr_client_label, 2, 0)
        grid.addWidget(self.nbr_client_value, 2, 1)
        grid.addWidget(self.start_serv, 3, 0)
        grid.addWidget(self.result, 4, 0)
        grid.addWidget(self.quitter, 7, 0)

        self.start_serv.clicked.connect(self.__demarrage)
        self.quitter.clicked.connect(self.actionQuitter)

        self.serveur_value.setText("0.0.0.0")
        self.port_value.setText('10000')
        self.nbr_client_value.setText('5')

    def __demarrage(self):
        self.result.setText("")
        self.start_serv.setText('Arrêt du serveur')
        self.serveur_value.setEnabled(False)
        self.port_value.setEnabled(False)
        self.nbr_client_value.setEnabled(False)
        accept = threading.Thread(target = MainWindow.__accept, args=[self])
        accept.start()

    def __accept(self, port = 4200):
        serveur_socket = socket.socket()
        serveur_socket.bind(('0.0.0.0', port))
        serveur_socket.listen()
        print("Serveur démarré")
        conn, address = serveur_socket.accept()
        print(f"Connexion établie avec {address}")
        MainWindow.reception(self, conn, serveur_socket)
        
    def reception(self, conn, socket):
        print(f"Ecoute en cours")
        while True:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"Nouveau message reçu : {message}")
            if message == "deco-server":
                reply = "Fin de la connexion"
                conn.send(reply.encode())
                print("Fin de la connexion avec le client")
                conn.close()
                socket.close()
                #MainWindow.deconnection(self)
                break

    def deconnection(self):
        self.result.setText("")
        self.start_serv.setText('Démarrage du serveur')
        self.serveur_value.setEnabled(True)
        self.port_value.setEnabled(True)
        self.nbr_client_value.setEnabled(True)

    def actionQuitter(self):
        QApplication.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()