import socket

class Cliente:
    """
    Clase para crear un cliente TCP/IP usando sockets
    Permite enviar mensajes al servidor
    """
    
    def __init__(self, ip='127.0.0.1', puerto=9001):  # Cambiado puerto de 8090 a 9001
        """
        Constructor de la clase Cliente
        
        Args:
            ip (str): Dirección IP del servidor (por defecto localhost)
            puerto (int): Puerto del servidor (cambiado a 9001)
        """
        self.ip = ip
        self.puerto = puerto
        # Crear socket TCP/IP
        # AF_INET: Familia de protocolos IPv4
        # SOCK_STREAM: Protocolo TCP (confiable)
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def enviar_mensaje(self):
        """
        Establece conexión con el servidor y envía un mensaje
        """
        self.cliente.connect((self.ip, self.puerto))
        mensaje = input("Escribe un mensaje para el servidor: ")
        self.cliente.send(mensaje.encode())
        print(f"Mensaje enviado exitosamente: '{mensaje}'")  # Print agregado como actividad extra
        self.cliente.close()

if __name__ == "__main__":
    # Crear instancia del cliente con puerto modificado
    cliente = Cliente(puerto=9001)  # Puerto cambiado como actividad extra
    cliente.enviar_mensaje()