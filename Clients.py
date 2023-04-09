import logging
import socket
import hashlib
import time
import os

# Define the folder where you want to save the file
folder_name = 'ArchivosRecibidos'

# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
if not os.path.exists('Logs'):
    os.mkdir('Logs')

# Set up logging
log_dir = 'Logs'
log_filename = time.strftime("%Y-%m-%d-%H-%M-%S-log.log.txt")
log_file_path = f'{log_dir}/{log_filename}'
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the server address and port 
# el valor de host es el ip del servidor
host = '127.0.0.1'
# port will be assigned by the server
port = 1025

sockets = []

# Create the client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
clientsocket.connect((host, port))
sockets.append(clientsocket)

# Receive the ready message from the server
ready_message = clientsocket.recv(1024).decode()

# Choose the file to receive from the server
filename = input('Enter the name of the file to receive (file1 or file2): followed by a coma and the number of clients required: ')

data = filename.split(',')


# Send the chosen filename to the server
clientsocket.send(filename.encode())
nombreArchivo = data[0]
clients = data[1]

allConnected = False

##connect all the clients to the server to receive the file, each client will be assigned a different port
#this is just for the first client, the rest of the clients will be connected in the receiveFile function
if allConnected == False:
        
    for i in range(2,int(clients)+1):
        logging.info(f'Connecting to server from client {i}')

        print('connecting to server from the client  '+str(i))
        clientsocketn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        port = 1025
        clientsocketn.connect((host, port))
        sockets.append(clientsocketn)
        ready_message = clientsocketn.recv(1024).decode()
        if ready_message == 'ready':
            print('Client '+ str(i)+'  connected to server')
            logging.info(f'Client {i} connected to server')
       
        else:
            print('Error connecting to server from the client  '+i)
            logging.error(f'Error connecting to server from client {i}')

    allConnected = True
    print('All clients required connected to server')
    logging.info('All required clients connected to server')

print('Receiving file from server')
print('receiving hash...')
## el hash se recibe en el cliente 1
file_hash = clientsocket.recv(1024).decode()
print(f'File hash: {file_hash}')
logging.info(f'File hash: {file_hash}')

file_contents = b''

bitsCounter = 0
if nombreArchivo == 'file1':
    file_size = 100000000
else:
    file_size = 250000000
while True:
    
    logging.info('Receiving data...'+ 'client 1')

    logging.info(f'Bits received so far: {bitsCounter}'+ 'client 1')

    print('receiving data...')
    print('bitscounter_: ' + str(bitsCounter))
    file_chunk = clientsocket.recv(1024 * 1024)
    file_contents += file_chunk
    bitsCounter += len(file_chunk)
    if not file_chunk or bitsCounter >= int(file_size):
        break
    
print('finished receiving data'+ 'client 1')
logging.info('Finished receiving data'+ 'client 1')

# Calculate the hash of the received file contents
received_hash = hashlib.sha256(file_contents).hexdigest()
filenameSave = 'Cliente-'+str(1)+'-Prueba-'+str(filename.split(',')[1]+'.txt')
    # Compare the received hash with the expected hash
if received_hash == file_hash:
    print('File hash matches')
    logging.info('File hash matches'+ 'client 1')

    # Save the received file to disk
    filenameSave = os.path.join(folder_name, filenameSave)

    with open(filenameSave, 'wb') as f:
        #save the file in a folder called ArchivosRecibidos
        filenameSave = os.path.join(folder_name, filename)

        f.write(file_contents)
    # Send a confirmation message to the server
    confirmation = 'received'
    clientsocket.send(confirmation.encode())
    print(f'File {filename} received and saved to disk')
    logging.info(f'File {filename} received and saved to disk of client 1')

else:
    # Send an error message to the server
    error_message = 'error'
    clientsocket.send(error_message.encode())
    print('File transfer error'+ 'client 1')
    logging.error('File transfer error'+ 'client 1')
clientsocket.close()  
sockets.pop(0)


def receiveFile(socket,numeroCliente):
    clientsocketN = socket
    print('Receiving file from server cliente: '+str(numeroCliente))
    logging.info(f'Receiving file from server client {numeroCliente}')
   
    print('receiving hash clients...')
    logging.info('Receiving hash from server')
    file_hash = ''
    ##el hash se termina hasta encontar \n
    
    file_hash = clientsocketN.recv(1024).decode()
        
    print(f'File hash: {file_hash}')
    file_contents = b''
    bitsCounter = 0
    while True:
        
        print ('receiving data...')
        logging.info(f'Receiving data from server client {numeroCliente}')
        print ('bitscounter_: '+str(bitsCounter))
        logging.info(f'Bits received so far: {bitsCounter}')
        file_chunk = clientsocketN.recv(1024 * 1024)
        file_contents += file_chunk
        bitsCounter += len(file_chunk)
        if not file_chunk or bitsCounter >= int(file_size):
            break
        
        #cycle is not finished until the file is received
    print('finished receiving data')
    logging.info(f'Finished receiving data from server client {numeroCliente}')
    # Calculate the hash of the received file contents
    received_hash = hashlib.sha256(file_contents).hexdigest()
    filenameSave = 'Cliente-'+str(numeroCliente)+'-Prueba-'+str(filename.split(',')[1]+'.txt')
        # Compare the received hash with the expected hash
    if received_hash == file_hash:
        print('File hash matches')
        logging.info(f'File hash matches from server client {numeroCliente}')
        # Save the received file to disk
        filenameSave = os.path.join(folder_name, filenameSave)
        with open(filenameSave, 'wb') as f:
            f.write(file_contents)
        # Send a confirmation message to the server
        confirmation = 'received'
        clientsocketN.send(confirmation.encode())
        print(f'File {filename} received and saved to disk')
        logging.info(f'File {filename} received and saved to disk of client {numeroCliente}')
    else:
        # Send an error message to the server
        error_message = 'error'
        clientsocketN.send(error_message.encode())
        print('File transfer error')
        logging.error(f'File transfer error from server client {numeroCliente}')
    clientsocketN.close()  
    
## reciveFile for the rest of the clients
numeroCliente=1
while len(sockets) > 0:
    numeroCliente+=1
    socket=sockets.pop(0)
    receiveFile(socket,numeroCliente)
    
allConnected = False






