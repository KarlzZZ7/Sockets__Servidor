import socket

class ClienteChatMejorado:
    """
    Clase para crear un cliente de chat TCP/IP mejorado
    Incluye retos adicionales: palabra clave personalizada, prefijos automáticos y colores
    """
    
    def __init__(self, ip='127.0.0.1', puerto=8090, palabra_salida="bye"):
        """
        Constructor de la clase ClienteChatMejorado
        
        Args:
            ip (str): Dirección IP del servidor
            puerto (int): Puerto del servidor
            palabra_salida (str): Palabra clave para terminar el chat (reto adicional)
        """
        self.ip = ip
        self.puerto = puerto
        self.palabra_salida = palabra_salida.lower()
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Códigos de colores ANSI (reto adicional)
        self.COLORES = {
            'ROJO': '\033[91m',
            'VERDE': '\033[92m',
            'AMARILLO': '\033[93m',
            'AZUL': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'BLANCO': '\033[97m',
            'RESET': '\033[0m'
        }
    
    def imprimir_color(self, texto, color='BLANCO'):
        """
        Imprime texto con color (reto adicional)
        
        Args:
            texto (str): Texto a imprimir
            color (str): Color del texto
        """
        print(f"{self.COLORES.get(color, self.COLORES['BLANCO'])}{texto}{self.COLORES['RESET']}")
    
    def iniciar_chat(self):
        """
        Conecta al servidor e inicia la conversación mejorada
        """
        try:
            # Conectar al servidor
            self.imprimir_color("=== CLIENTE DE CHAT MEJORADO ===", 'CYAN')
            self.imprimir_color(f"Conectando al servidor {self.ip}:{self.puerto}...", 'AMARILLO')
            
            self.cliente.connect((self.ip, self.puerto))
            
            self.imprimir_color("Conexión establecida con el servidor.", 'VERDE')
            self.imprimir_color(f"Chat iniciado. Escribe '{self.palabra_salida}' para terminar.", 'AZUL')
            self.imprimir_color("-" * 60, 'MAGENTA')
            
            while True:
                # Enviar mensaje al servidor con prefijo automático
                mensaje = input(f"{self.COLORES['AZUL']}Cliente dice: {self.COLORES['RESET']}")
                
                # Validar que el mensaje no esté vacío
                if not mensaje.strip():
                    self.imprimir_color("El mensaje no puede estar vacío. Intenta de nuevo.", 'AMARILLO')
                    continue
                
                self.cliente.send(mensaje.encode('utf-8'))
                
                # Verificar comando de salida personalizado
                if mensaje.lower() == self.palabra_salida:
                    self.imprimir_color("Cliente cerró la conexión.", 'ROJO')
                    break
                
                # Recibir respuesta del servidor
                try:
                    respuesta = self.cliente.recv(1024).decode('utf-8')
                    
                    if not respuesta:
                        self.imprimir_color("El servidor se desconectó inesperadamente.", 'ROJO')
                        break
                    
                    # Verificar si el servidor quiere cerrar
                    if respuesta.lower() == self.palabra_salida:
                        self.imprimir_color("El servidor ha cerrado la conexión.", 'ROJO')
                        break
                    
                    # Mostrar respuesta del servidor con prefijo automático y color
                    self.imprimir_color(f"Servidor dice: {respuesta}", 'VERDE')
                    
                except ConnectionResetError:
                    self.imprimir_color("El servidor se desconectó inesperadamente.", 'ROJO')
                    break
                except Exception as e:
                    self.imprimir_color(f"Error al recibir mensaje: {e}", 'ROJO')
                    break
                    
        except ConnectionRefusedError:
            self.imprimir_color("Error: No se pudo conectar al servidor.", 'ROJO')
            self.imprimir_color("Verifica que el servidor esté ejecutándose.", 'AMARILLO')
        except Exception as e:
            self.imprimir_color(f"Error en el cliente: {e}", 'ROJO')
        finally:
            self.cliente.close()
            self.imprimir_color("Cliente cerrado.", 'AMARILLO')

if __name__ == "__main__":
    # Crear instancia del cliente de chat mejorado
    # Reto adicional: palabra clave personalizada "bye" en lugar de "salir"
    cliente = ClienteChatMejorado(palabra_salida="bye")
    cliente.iniciar_chat()