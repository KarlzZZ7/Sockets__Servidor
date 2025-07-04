import socket
import threading  # Se importó threading para el RETO 4: múltiples clientes

class ServidorChat:
    def __init__(self, ip='127.0.0.1', puerto=8090):
        self.ip = ip
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se configuró la reutilización de dirección para evitar errores
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # =========================
        # RETO 1: CAMBIO DE PALABRA CLAVE
        # =========================
        # Se cambió la palabra clave de "salir" a "bye"
        self.palabra_salida = "bye"
        
        # =========================
        # RETO 3: COLORES EN CONSOLA
        # =========================
        # Se definieron códigos de colores ANSI para la consola
        self.colores = {
            'RESET': '\033[0m',      # Se definió código para resetear color
            'ROJO': '\033[91m',      # Se definió código para color rojo (errores)
            'VERDE': '\033[92m',     # Se definió código para color verde (éxito)
            'AMARILLO': '\033[93m',  # Se definió código para color amarillo (advertencias)
            'AZUL': '\033[94m',      # Se definió código para color azul (información)
            'MAGENTA': '\033[95m',   # Se definió código para color magenta (decoración)
            'CYAN': '\033[96m'       # Se definió código para color cyan (mensajes)
        }
        
        # =========================
        # RETO 4: MÚLTIPLES CLIENTES
        # =========================
        # Se creó lista para almacenar clientes conectados
        self.clientes_conectados = []
    
    def imprimir_con_color(self, mensaje, color='RESET'):
        """
        RETO 3: COLORES EN CONSOLA
        Se creó método para imprimir mensajes con colores
        """
        # Se concatenó el código de color con el mensaje y el reset
        print(f"{self.colores[color]}{mensaje}{self.colores['RESET']}")
    
    def manejar_cliente(self, conexion, direccion):
        """
        RETO 4: MÚLTIPLES CLIENTES
        Se creó método para manejar cada cliente por separado
        """
        # RETO 3: Se mostró mensaje de conexión con color verde
        self.imprimir_con_color(f"Cliente {direccion} se conectó al chat", 'VERDE')
        
        try:
            while True:
                # Se recibieron datos del cliente
                datos = conexion.recv(1024).decode('utf-8')
                
                # Se verificó si el cliente se desconectó inesperadamente
                if not datos:
                    # RETO 3: Se mostró mensaje de desconexión con color rojo
                    self.imprimir_con_color(f"Cliente {direccion} se desconectó", 'ROJO')
                    break
                
                # =========================
                # RETO 1: CAMBIO DE PALABRA CLAVE
                # =========================
                # Se verificó la nueva palabra clave "bye" en lugar de "salir"
                if datos.lower() == self.palabra_salida:
                    # RETO 3: Se mostró mensaje de cierre con color rojo
                    self.imprimir_con_color(f"Cliente {direccion} cerró la conexión con '{self.palabra_salida}'", 'ROJO')
                    break
                
                # =========================
                # RETO 2: PREFIJOS AUTOMÁTICOS
                # =========================
                # Se agregó prefijo automático "Cliente dice:"
                # RETO 3: Se mostró mensaje del cliente con color cyan
                self.imprimir_con_color(f"Cliente {direccion} dice: {datos}", 'CYAN')
                
                # =========================
                # RETO 2: PREFIJOS AUTOMÁTICOS
                # =========================
                # Se solicitó respuesta del servidor con prefijo automático "Servidor dice:"
                # RETO 3: Se mostró prompt del servidor con color amarillo
                print(f"{self.colores['AMARILLO']}Servidor dice (para {direccion}): {self.colores['RESET']}", end="")
                mensaje = input()
                
                # Se envió mensaje del servidor al cliente
                conexion.send(mensaje.encode('utf-8'))
                
                # =========================
                # RETO 1: CAMBIO DE PALABRA CLAVE
                # =========================
                # Se verificó si el servidor quiere cerrar con la nueva palabra "bye"
                if mensaje.lower() == self.palabra_salida:
                    # RETO 3: Se mostró mensaje de cierre con color rojo
                    self.imprimir_con_color(f"Servidor cerró conexión con {direccion}", 'ROJO')
                    break
                    
        except Exception as e:
            # RETO 3: Se manejó cualquier error con color rojo
            self.imprimir_con_color(f"Error con cliente {direccion}: {e}", 'ROJO')
        finally:
            # Se cerró la conexión del cliente
            conexion.close()
            # RETO 4: Se removió cliente de la lista de conectados
            if conexion in self.clientes_conectados:
                self.clientes_conectados.remove(conexion)
            # RETO 3: Se mostró mensaje de terminación con color amarillo
            self.imprimir_con_color(f"Conexión con {direccion} terminada", 'AMARILLO')
    
    def iniciar_chat(self):
        """Se modificó método para implementar todos los retos"""
        try:
            # Se vinculó el servidor a la dirección y puerto
            self.servidor.bind((self.ip, self.puerto))
            
            # =========================
            # RETO 4: MÚLTIPLES CLIENTES
            # =========================
            # Se cambió a 5 conexiones para permitir múltiples clientes
            self.servidor.listen(5)
            
            # =========================
            # RETO 3: COLORES EN CONSOLA
            # =========================
            # Se mostró mensaje de inicio con colores
            self.imprimir_con_color("="*50, 'MAGENTA')
            self.imprimir_con_color("🚀 SERVIDOR DE CHAT MEJORADO INICIADO", 'VERDE')
            self.imprimir_con_color(f"📡 Escuchando en {self.ip}:{self.puerto}", 'AZUL')
            
            # =========================
            # RETO 1: CAMBIO DE PALABRA CLAVE
            # =========================
            # Se mostró información sobre la nueva palabra clave "bye"
            self.imprimir_con_color(f"🔑 Palabra para salir: '{self.palabra_salida}'", 'AMARILLO')
            
            # RETO 3: Se mostró información con colores
            self.imprimir_con_color("👥 Esperando clientes... (CTRL+C para cerrar servidor)", 'CYAN')
            self.imprimir_con_color("="*50, 'MAGENTA')
            
            # =========================
            # RETO 4: MÚLTIPLES CLIENTES
            # =========================
            # Se implementó bucle para aceptar múltiples clientes
            while True:
                try:
                    # Se aceptó nueva conexión de cliente
                    conexion, direccion = self.servidor.accept()
                    # Se agregó cliente a la lista de conectados
                    self.clientes_conectados.append(conexion)
                    
                    # Se creó hilo separado para manejar cada cliente
                    hilo_cliente = threading.Thread(
                        target=self.manejar_cliente, 
                        args=(conexion, direccion)
                    )
                    # Se configuró el hilo como daemon para que termine con el programa principal
                    hilo_cliente.daemon = True
                    # Se inició el hilo del cliente
                    hilo_cliente.start()
                    
                except KeyboardInterrupt:
                    # Se capturó interrupción del usuario (CTRL+C)
                    # RETO 3: Se mostró mensaje de cierre con color rojo
                    self.imprimir_con_color("\n🛑 Cerrando servidor...", 'ROJO')
                    break
                    
        except Exception as e:
            # RETO 3: Se manejó cualquier error del servidor con color rojo
            self.imprimir_con_color(f"❌ Error en el servidor: {e}", 'ROJO')
        finally:
            # RETO 4: Se cerraron todas las conexiones de clientes
            for cliente in self.clientes_conectados:
                try:
                    cliente.close()
                except:
                    pass
            # Se cerró el socket del servidor
            self.servidor.close()
            # RETO 3: Se mostró mensaje de cierre con color amarillo
            self.imprimir_con_color("🔒 Servidor cerrado completamente", 'AMARILLO')

if __name__ == "__main__":
    # Se creó instancia del servidor con todos los retos implementados
    servidor = ServidorChat()
    # Se inició el chat
    servidor.iniciar_chat()