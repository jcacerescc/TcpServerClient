# Servidor TCP


1.Para ejecutar, debe tener en la misma carpeta del servidor los archivos a compartir, el de 100mb y el de 250mb, especificamente estos archivos deben estar nombrados como  '100mb' y '250mb'. Para generar archivos de la cantidad especificada y que el servidor pueda correr puede hacer uso de la siguiente web : https://generatefile.com/
Descargue esete repositorio en dos maquinas diferentes, una sera la encargada de manejar el servidor y la otra los clientes.

2.Asegurese de que el host definido en el archivo Server.py y Clients.py sea la ip de la maquina en la que se va a ejecuar el servidor.

3.Corra con el comando 'python Server.py' en el terminal de la maquina en la que ejecutara el servidor para que el mismo empiece a ejecutarse

4.Corra con el comando 'python Clients.py' en el terminal de la maquina en la que ejecutara el cliente para que el mismo empiece a ejecutarse. Revise que la ip definida en el atributo host, corresponda a la ip de la maquina en la que esta ejecutando el servidor.

5. El cliente le pedira que escriba el archivo que quiere transferir('File1' para el archivo de 100mb)y ('File2' para el archivo de 250mb), seguido de una coma ',' y el numero de clientes al que quiere transferir (Maximo 25)

* Ejemplos de entrada podria ser'File1,20' y 'File2,6'.

6.El servidor empezara enviar el archivo a los distintos clientes, los diferentes registros de actividad quedaran registrados en la consola y en los archivos log.
