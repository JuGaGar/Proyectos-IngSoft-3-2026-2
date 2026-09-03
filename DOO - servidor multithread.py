from socket import *
import threading

#Constantes relevantes
HOST ='localhost' #Dirección host (IP o local)
PORT = 5050          #Puerto de servicio
BUFFER = 500         #Buffer máximo de datos a recibir
QUEUE = 40

def main():
    #Crear y abrir socket
    srv = socket(AF_INET, SOCK_STREAM)
    srv.bind((HOST, PORT))
    srv.listen(QUEUE) #Cola máxima
    print('Servidor escuchando en ' + str(HOST) + ':' + str(PORT))

    #Esperar cliente y crear hilo
    while True:
        client, addr = srv.accept()
        thread = threading.Thread(target=handleClient, args=(client, addr))
        thread.start()
        print('Conexiones activas: ' + str(threading.active_count() - 1))

def handleClient(client, addr):
    #Notificar conexión nueva
    print('Conexión desde '+ str(addr))

    #Recibir y decodificar mensaje de cliente
    cInput = client.recv(BUFFER).decode('utf-8')

    #Validar condiciones
    letters = 'abcdefghijklmnñopqrstuvwxyz ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    validInput=True
    for char in cInput:
        if char not in letters:
            print('Hilo inválido. Caractér no permitido encontrado: ' + char)
            validInput=False
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
    main()