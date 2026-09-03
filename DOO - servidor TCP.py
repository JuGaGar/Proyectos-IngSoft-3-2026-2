from socket import *
import threading

def start_server():
    #Dirección y puerto
    host ='localhost' #Dirección host (IP o local)
    port = 5050       #Puerto de servicio
    buffer = 500      #Buffer máximo de datos a recibir/enviar
    queue = 40         #Longitud máxima de cola

    #Crear socket
    srv = socket(AF_INET, SOCK_STREAM)

    #Asociar socket a dirección y puerto
    srv.bind((host, port))

    #Empezar operación y máximo de conexiones enlistadas permitidas
    srv.listen(queue)
    print('Servidor escuchando en ' + str(host) + ':' + str(port))

    #Ciclo de operación
    while True:
        #Esperar cliente y confirmar conexión
        client, addr = srv.accept()
        print('Conexión desde '+ str(addr))

        #Recibir y decodificar mensaje de cliente
        cInput = client.recv(buffer).decode('utf-8')

        #Validar condiciones
        letters = 'abcdefghijklmnñopqrstuvwxyz ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
        validInput=True
        for char in cInput:
            if char not in letters:
                print('Hilo inválido. Caractér no permitido encontrado: ' + char)
                validInput=False
                client.close()
            else:
                pass

        #Acción si se validó correctamente
        if(validInput):
            #Procesar mensaje de cliente y crear respuesta
            lastChar = cInput[-1]
            charCount = 0
            for char in cInput:
                if char == lastChar:
                    charCount+=1
            sOutput = charCount

            #Devolver respuesta
            client.send(str(sOutput).encode('utf-8'))

            #Registrar en archivo
            with open(r"C:\Users\jugag\Desktop\Coding\Proyectos UIS\DOO\registro cadenas.txt", mode="a", newline='') as file:
                file.write(str(cInput) + ' : ' + str(charCount) + '\n')
            
            #Resumen
            print('')
            print('Recibido: '+ str(cInput))
            print('Caracter final:' + str(lastChar))
            print('Veces que aparece:' + str(charCount))

            #Cerrar conexión
            client.close()

if __name__ == '__main__':
    start_server()