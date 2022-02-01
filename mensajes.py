# Importamos el ModuMódulo
import pywhatkit 
from datetime import datetime, date

telefono = "+5493364537093"
message = "Señor Cliente, Mafelectric le informa que la Reparación de su Artefacto, ingresado con Nº de orden: 103 esta finalizada "
message += "Por favor pase a Retirarlo, Muchas Gracias ... . Puede seguir el el estado de sus reparaciones ingresando a http://mafelectric.com.ar"

hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
hora = int(hoy[11:13])
minuto = int(hoy[14:16]) + 1


def mensaje(telefono, message, hora, min):
    print(telefono)
    print(message)
    print(hora)
    print(minuto)
   # Usamos Un try-except
    try: 
        # Enviamos el mensaje 
        pywhatkit.sendwhatmsg(telefono, mensaje, hora, minuto) 
        print("Mensaje Enviado") 
    except: 
        print("Ocurrio Un Error")

mensaje(telefono, message, hora, min)