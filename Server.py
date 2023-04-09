import datetime
import socket
import logging
import hashlib
import time
import os
#El nombre del archivo de Logs debe incluir la fecha exacta de la prueba. Ejemplo: <año- mes-dia-hora-minuto-segundo-log.txt>
file_logname = time.strftime("%Y-%m-%d-%H-%M-%S-.logServer.txt")

logging.basicConfig(filename=file_logname, # set a static filename
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


#Creating the socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#el host debe ser la IP del servidor
host = '127.0.0.1' #Host is the server IP
port = 1025 #Port to listen on 

#Binding to socket
serversocket.bind((host, port)) #Host will be replaced/substitued with IP, if changed and not running on host

#Starting TCP listener
serversocket.listen(25)

# Define the files to be sent
files = {
    
    'file1': {'path': '100mb.txt', 'size': 0},
    'file2': {'path': '250mb.txt', 'size': 0}

}
#get the size of the files

for file in files:
    files[file]['size'] = os.path.getsize(files[file]['path'])

print('files: '+str(files))    
# Initialize a list to store the client sockets
client_sockets = []




# Wait for the first client to connect and send the file name and number of clients required
first_client_socket = None
while first_client_socket is None:
    clientsocket, address = serversocket.accept()
    logging.info('Connection received from %s', str(address))
    if len(client_sockets) == 0:
        # Send a ready message to the client
        ready_message = 'ready'
        clientsocket.send(ready_message.encode())
        # Wait for the client to send the file name and number of clients required
        message = clientsocket.recv(1024).decode()
        file_choice, num_clients_required = message.split(",")
        num_clients_required = int(num_clients_required)
        # Set the first client socket as the socket of the client who sent the file name and number of clients required
        first_client_socket = clientsocket
        print('first '+ str(num_clients_required))
        # Add the client socket to the list
        client_sockets.append(clientsocket)
        print('client 1 connected and added to the list')
        print('\n sockets'+str(client_sockets))
    else:
        # Reject the connection from the client as the first client has not yet connected
        reject_message = 'reject'
        clientsocket.send(reject_message.encode())
        # Close the connection
        clientsocket.close()

# Get the file path and size
file_path = files[file_choice]['path']
file_size = files[file_choice]['size']

# Wait for all clients to be ready
for i in range(2, num_clients_required+1):
    print('waiting for client'+str(i))
    
    clientsocket, address = serversocket.accept()
    
    logging.info('Connection received from %s', str(address))
    client_sockets.append(clientsocket)
    print('client '+str(i)+' connected and added to the list')
    ready_message = 'ready'
    
    clientsocket.send(ready_message.encode())
print('all clients requiered connected to the server')

def send_file(file_path, file_size, clientsocket, i):
    counterbytes = 0
    # Send the file hash 
    hash_message = file_hash
    print('hash message: '+str(hash_message+str(i+1)))
    message=hash_message
    clientsocket.send(message.encode())
    print('hash sent:'+str(hash_message))
    
    with open(file_path, 'rb') as f:
            time.sleep(0.5)
            start_time = time.time()
            while True:
                #set a waiting time for the client to be ready to receive the file
                
                
                ##send the file in chunks
                file_chunk = f.read(1024 * 1024)
                clientsocket.send(file_chunk)
                ##update the counter
                counterbytes += len(file_chunk)
                ##print the progress
                print('Sent: ', counterbytes, 'bytes')
                ## if the file is sent, break the loop
                if counterbytes == file_size:
                    break
            print('file sent')
            end_time = time.time()
            confirmation = clientsocket.recv(1024).decode()
            print('confirmation: '+str(confirmation))    
            if confirmation == 'received':
                ##register the date and time of the transfer
                logging.info('File %s (%d bytes) sent to client %d in %.2f seconds, Date and time of the transfer: %s', file_path, file_size, i, end_time - start_time, datetime.datetime.now())
            else:
                logging.info('File %s (%d bytes) delivery to client %d failed', file_path, file_size, i)

    

# Calculate the file hash
with open(file_path, 'rb') as f:
    file_contents = f.read()
    print('file readed')
    file_hash = hashlib.sha256(file_contents).hexdigest()
    print('hash: '+str(file_hash))



# Send the file to each client

print ('sending file to clients')
print ('client sockets: '+str(enumerate(client_sockets)))
for i, clientsocket in enumerate(client_sockets):
    print('sending file to client '+str(i+1))
    send_file(file_path, file_size, clientsocket, i)
    # Close the connection
    clientsocket.close()
   

# Clear the client socket list for the next file transfer
client_sockets.clear()
