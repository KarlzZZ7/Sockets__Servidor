import socket

class Servidor:
    """
    Clase para crear un servidor TCP/IP usando sockets
    Permite recibir mensajes de clientes conectados
    """
    
    def __init__(self, ip='127.0.0.1', puerto=9001):  # Cambiado puerto de 8090 a 9001
        """
        Constructor de la clase Servidor
        
        Args:
            ip (str): Dirección IP del servidor (por defecto localhost)
            puerto (int): Puerto donde escuchará el servidor (cambiado a 9001)
        """
        self.ip = ip
        self.puerto = puerto
        # Crear socket TCP/IP
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def iniciar(self):
        """
        Inicia el servidor y espera conexiones de clientes
        """
        self.servidor.bind((self.ip, self.puerto))
        self.servidor.listen(5)
        print(f"Servidor escuchando en {self.ip}:{self.puerto}")
        conexion, direccion = self.servidor.accept()
        print("Conexión establecida con:", direccion)
        datos = conexion.recv(1024)
        print("Mensaje recibido:", datos.decode())
        conexion.close()

if __name__ == "__main__":
    # Crear instancia del servidor con puerto modificado
    servidor = Servidor(puerto=9001)  # Puerto cambiado como actividad extra
    servidor.iniciar()