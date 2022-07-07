import os
#from aes import AES  # importa las funciones ya hechas del código de aes, no se usan ya que lo va a ser el FPGA
import tkinter  # importa la librería tkinter, que es la base de la cual se crea la interfaz de usuario
import \
    serial  # importa la librería serial, que tiene las funciones para poder lograr una comunicación serial entre la interfaz y el FPGA
import serial.tools.list_ports  # importa la librería serial.tools.lists_ports que nos da la información de los puertos


def get_ports():  # función para obtener puertos
    ports = serial.tools.list_ports.comports()  # Esto hace que ports tenga la lista de puertos del dispositivo
    print(ports)

    return ports  # devuelve ports, que es una lista con los puertos


def Hallar_FPGA(portsFound):  # Función para hallar en que puerto está conectado el FPGA
    commPort = 'None'  # Este es el puerto de comunicación, que donde debe estar conectado el FPGA. Empieza con None en caso no esté conectado ningún FPGA
    numConnection = len(portsFound)  # numConection es el número de conecciones totales que tiene nuestro dispositivo

    for i in range(0, numConnection):  # El rango abarca hasta el número total de puertos
        port = foundPorts[
            i]  # port va a tomar el valor de cada puerto para analizar si este puerto es donde esta conectado el FPGA
        strPort = str(port)  # Vuelve un string el valor de port para ver si este coincide con el nombre del FPGA

        if 'USB' in strPort:  # Si coincide, va a tomar este puerto
            splitPort = strPort.split(' ')  # Divide toda la oración del puerto en una lista de strings, donde toma un espacio como una separación.
            commPort = (splitPort[
                0])  # Agarra el primer valor de la lista de palabras que decribe al puerto donde esta el FPGA, siendo este el número del puerto donde esta conectado
    return commPort  # Devuelve el número de puerto donde se hace la comunicación del FPGA y el dispositivo


def other_ports():  # Esta función está hecha para dar los otros puertos donde no está conectado el FPGA
    texto_a_retornar = ""  # Este es el texto que se devolverá con la información de los puertos que
    total_ports = get_ports()  # Esta variable tiene la lista de puertos del dispositivo
    puerto_conectado = Hallar_FPGA(total_ports)  # Esta variable  nos da el puerto donde está conectado el FPGA
    for i in range(0, len(total_ports)):  # El rango va de 0 hasta el número total de puertos en el dispositivo
        port = total_ports[i]  # port va a tomar el valor de cada puerto para analizarlo
        strPort = str(port)  # Se vuelve string al puerto para poder hacer la comparación
        if "USB" in strPort:  # Aquí revisa si el puerto evualado es donde está el FPGA (dice Arduino por mientras hasta que sepa el nombre del puerto del FPGA al conectarse)
            continue  # Continua si es el puerto donde esta conectado el FPGA, salteandose el else
        else:
            splitPort = strPort.split(
                ' ')  # Caso contrario el puerto analizado no tenga el FPGA conectado, se divide esta oración con información del puerto en una lista con las palabras, siendo el espacio (' ') lo que separa las palabras
            texto_a_retornar = texto_a_retornar + splitPort[
                0] + "\n"  # Esto nos da el nombre del puerto donde no está conectado y pone un enter después por si hay más puertos a analizar
    return texto_a_retornar  # Devuelve la lista (o mejor dicho un string que los nombra) con el total de puertos exceptuando el puerto donde está conectado el FPGA


def encriptar():  # Función para encriptar usando la función ya hecha del AES en el FPGA
    mensaje_a_encriptar = bytes(mensaje_a_recibir.get(),
                                "UTF-8")  # obtiene el mensaje del usuario, que en este caso es el mensaje que este desea encriptar, y lo transforma en bytes
    Puerto_serial.write(mensaje_a_encriptar)  # Esta función manda el mensaje del usuario por puerto serial hacia el FPGA
    mensaje_encriptado = Puerto_serial.readline().decode("ascii")  # mensaje_encriptado usa una función recibe el mensaje en binario por el puerto serial. Luego, lo transforma usando el código ascii en una palabra
    #mensaje_encriptado = AES(clave).encrypt_ctr(mensaje_a_encriptar, vi) #Esto es por si se quiere probar con la misma librería de AES ya creada de python, no es necesaria debido a que el proceso lo va a hacer el FPGA
    mensaje_a_devolver_encriptado.config(text=mensaje_encriptado)  # modifica el texto que muestra el objeto ttk.Label de mensaje_a_devolver_encriptado para que muestre el mensaje ya encriptado

def desencriptar():  # función para desencriptar ya hecha en el PGA, esta función falta agregarle la forma en que el mismo FPGA distinga entre si el mensaje que se envía es para encriptar o para desencriptar, esto de hará después
    mensaje_a_desencriptar = bytes(mensaje_a_recibir.get(), "UTF-8")  #Obtiene el mensaje a desencriptar del usuario
    #mensaje_desencriptado = AES(clave).decrypt_ctr(mensaje_a_desencriptar, vi)  #En caso se quiera probar con el código de AES de python, se usa esto. Sin embargo, el proceso se va a dar en el FPGA, por lo que esta linea queda obsoleta
    Puerto_serial.write(mensaje_a_desencriptar)  #Envía el mensaje por serial al FPGA
    mensaje_desencriptado = Puerto_serial.readline().decode("ascii")  #Recibe el mensaje en binario y lo transforma usando ascii en la frase ya desenciptada
    mensaje_a_devolver_desencriptado.config(text=mensaje_desencriptado)  #Transforma el mensaje que muestra el objeto ttk.Label mensaje_a_devolver_desencriptado en el mensaje ya desenciptado por AES


def buscar_puertos():  # función que busca actualizar si los puertos han sido modificados. Actualmente no he podido comprobar que funciona, pero teóricamente debería
    foundPorts = get_ports()  # Esta variable almacena una lista con los puertos
    connectPort = Hallar_FPGA(
        foundPorts)  # Obtiene el puerto donde se encuentra el FPGA, caso contrario, esta variable tiene como valor "None"
    if connectPort != 'None':  # Si es que hay un puerto conectado con el FPGA, se actualizar la variable Puerto_serial, que es la variable que permite la conexión serial
        cambiar_puerto(connectPort)  # actualizar la información del puerto serial
    puertos_libres = other_ports()  # Devuelve la lista (o mejor dicho un string que los nombra) con el total de puertos exceptuando el puerto donde está conectado el FPGA
    Puerto_conectado.config(
        text=connectPort)  # Actualiza el mensaje que muestra puerto_conectado con el puerto donde esta ahora conectado el FPGA
    Puertos_no_conectados.config(
        text=puertos_libres)  # Actualiza el mensaje que muestra puerto_conectado con los nuevos puertos donde no está el FPGA

def cambiar_puerto(Puerto_nuevo): #función para cambiar el puerto serial
    global Puerto_serial
    Puerto_serial= ""
    Puerto_serial = serial.Serial(Puerto_nuevo, baudrate=9600, timeout=1) #hace una conexión serial dese el puerto donde se encuentra conectado el FPGA


foundPorts = get_ports()  # Obtiene una lista con los puertos en el dispositivo
connectPort = Hallar_FPGA(foundPorts)  # Obtiene el numero de puerto donde esta conectado el FPGA
puertos_libres = other_ports()  # Obtiene una lista (o mejor dicho un string que los nombra) con el total de puertos exceptuando el puerto donde está conectado el FPGA
if connectPort != 'None':  # Analiza si hay un FPGA conectado
    Puerto_serial = serial.Serial(connectPort, baudrate=9600,
                                  timeout=1)  # Hace una variable que representa la conexión serial entre el dispositvo y el FPGA, con el puerto donde se encuentra, el ratio da batios y el timeout que hay para obtener algún dato
#clave = b'!l\xa4\x8cEzu\xb31\xe6k\xc3%\xabB\x03'
#Clave generada usando el código de AES de python, debido a que este proceso se hará en el FPGA, esta linea ya no es necesaria
#vi = b']\x1a\x0ejI&\xf8~\xde\xf2\x06\x87\xd5\xbc\xfa\xb7'
#Vi generada usando el código de AES de python, debido a que este proceso se hará en el FPGA, esta linea ya no es necesaria
#print(clave)
#print(vi)
root = tkinter.Tk()  # Crea un objeto ttk del tipo Tk que representa a la ventana que se va a crear
root.config(width=700, height=475)  # Ajusta el tamaño de la ventana en su largo y ancho en pixeles
root.title("Encriptación AES")  # Le pone un nombre a la ventana, en este caso "Encriptación AES"
root.config(background="lightyellow")  # Le pone un color de fondo a la ventana, en este caso es amarillo claro
titulo = tkinter.Label(root, text="Encriptación usando AES", font=("Times", 30, "bold"), fg="orange",
                       background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Encriptación usando AES", la fuente Times New Roman con tamaño 30 y en negritas, con el color de letras naranja, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
indicacion = tkinter.Label(root, text="Introduce abajo el texto a encriptar", font=("Times", 16), fg="purple",
                           background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Introduce abajo el texto a encriptar", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
mensaje_a_recibir = tkinter.Entry(root, font=("Times", 12),
                                  width=40)  # Crea un objeto tkinter.Entry que es donde el usuario va a introducir su mensaje para encriptar/desencriptar. Tiene como fuente las letras que se escriban de Times New Roman con tamaño 12 y el ancho de letras que va a poner visualizarse al mismo tiempo al escribir es 40 (al especificar el tamaño de letras menor al default, se pueden visualizar mas letras)
boton_encriptar = tkinter.Button(root, text="Encriptar", command=encriptar, width=15, height=3, background="orange",
                                 font=("times", 16), relief=tkinter.FLAT,
                                 activebackground="green")  # Crea un objeto tkinter.Button que se encarga de llamar a una función cuando se presiona. El botón tiene como texto "Encriptar", al presionarse hace la funcion encriptar, tiene un tamaño de ancho de 15 letras, tiene un tamaño de altura de 3 letras, tiene fondo naranja, tiene de guente Times New Roman de tamaño 16, tiene relieve plano y al presionarse se cambia el color a verde
boton_desencriptar = tkinter.Button(root, text="Desencriptar", command=desencriptar, width=15, height=3,
                                    background="orange",
                                    font=("times", 16), relief=tkinter.FLAT,
                                    activebackground="green")  # Crea un objeto tkinter.Button que se encarga de llamar a una función cuando se presiona. El botón tiene como texto "Desencriptar", al presionarse hace la funcion encriptar, tiene un tamaño de ancho de 15 letras, tiene un tamaño de altura de 3 letras, tiene fondo naranja, tiene de guente Times New Roman de tamaño 16, tiene relieve plano y al presionarse se cambia el color a verde
indicacion_MEncriptado = tkinter.Label(root, text="Mensaje encriptado:", font=("Times", 16), fg="purple",
                                       background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Mensaje encriptado: ", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
indicacion_MDesencriptado = tkinter.Label(root, text="Mensaje desencriptado:", font=("Times", 16), fg="purple",
                                          background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Mensaje desencriptado: ", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
mensaje_a_devolver_encriptado = tkinter.Label(root, fg="black",
                                              background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Mensaje encriptado: ", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
mensaje_a_devolver_desencriptado = tkinter.Label(root, fg="black",
                                                 background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene el color de letras negro y el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
Puerto_conectado = tkinter.Label(root, fg="black", text=connectPort,
                                 background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje el número del puerto donde está conectado el FPGA, el color de letras negro y el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
Puertos_no_conectados = tkinter.Label(root, fg="black", text=puertos_libres,
                                      background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje el número del puertos exceptuando el puerto donde está conectado el FPGA, el color de letras negro y el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
mensaje_puerto_conectado = tkinter.Label(root, text="Puerto conectado:", font=("Times", 16), fg="purple",
                                         background="lightyellow")  # Crea un objeto tkinter.Label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Puerto conectado: ", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
mensaje_puertos_no_conectados = tkinter.Label(root, text="Puertos libres:", font=("Times", 16), fg="purple",
                                              background="lightyellow")  # Crea un objeto tkinter.label que se encarga de mostrar un mensaje en la ventana. En este caso tiene como mensaje "Puertos libres: ", la fuente Times New Roman con tamaño 16, con el color de letras morado, y por último el fondo del Label va a ser amarillo claro para que combine con el fondo de la ventana
boton_serial = tkinter.Button(root, text="Actualizar puertos", command=buscar_puertos(), width=15, height=3,
                              background="orange",
                              font=("times", 16), relief=tkinter.FLAT,
                              activebackground="green")  # Crea un objeto tkinter.Button que se encarga de llamar a una función cuando se presiona. El botón tiene como texto "Actualizar puertos", al presionarse hace la funcion encriptar, tiene un tamaño de ancho de 15 letras, tiene un tamaño de altura de 3 letras, tiene fondo naranja, tiene de guente Times New Roman de tamaño 16, tiene relieve plano y al presionarse se cambia el color a verde
root.bind("<Return>",
          lambda event: encriptar())  # Esta función hace que al presionar enter se inicie la función encriptar
titulo.place(x=150,
             y=0)  # Pone el titulo en 150 pixeles a la derecha contando desde la esquina superior izquierda de la ventana a crear
indicacion.place(x=218,
                 y=70)  # Pone la indicacion en 218 pixeles a la derecha y 70 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
mensaje_a_recibir.place(x=200,
                        y=100)  # Pone el mensaje_a_recibir en 200 pixeles a la derecha y 100 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
boton_encriptar.place(x=165,
                      y=150)  # Pone el boton_encriptar en 165 pixeles a la derecha y 150 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
boton_desencriptar.place(x=385,
                         y=150)  # Pone el boton_desencriptar en 385 pixeles a la derecha y 150 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
indicacion_MEncriptado.place(x=100,
                             y=260)  # Pone la indicacion_MEncriptado en 100 pixeles a la derecha y 260 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
indicacion_MDesencriptado.place(x=100,
                                y=310)  # Pone la indicacion_MDesencriptado en 100 pixeles a la derecha y 310 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
mensaje_a_devolver_encriptado.place(x=269,
                                    y=265)  # Pone el mensaje_a_devolver_encriptado en 269 pixeles a la derecha y 265 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
mensaje_a_devolver_desencriptado.place(x=295,
                                       y=315)  # Pone el mensaje_a_devolver_desencriptado en 295 pixeles a la derecha y 315 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
mensaje_puerto_conectado.place(x=100,
                               y=365)  # Pone el mensaje_puerto_conectado en 100 pixeles a la derecha y 365 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
mensaje_puertos_no_conectados.place(x=100,
                                    y=415)  # Pone el mensaje_puertos_no_conectados en 100 pixeles a la derecha y 415 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
Puerto_conectado.place(x=265,
                       y=370)  # Pone el Puerto_conectado en 265 pixeles a la derecha y 370 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
Puertos_no_conectados.place(x=240,
                            y=410)  # Pone el Puertos_no_conectados en 240 pixeles a la derecha y 410 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
boton_serial.place(x=350,
                   y=370)  # Pone el Boton_serial en 350 pixeles a la derecha y 370 pixeles hacia abajo, contando desde la esquina superior izquierda de la ventana a crear
root.mainloop()  # Hace que el root que es la ventana a crear se ponga en un loop hasta que se cierre la ventana,
