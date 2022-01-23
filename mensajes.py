# Importamos el ModuMódulo

import pywhatkit 
def mensaje(telefono,mensaje, hora, min):

    # Usamos Un try-except
    try: 

        # Enviamos el mensaje

        pywhatkit.sendwhatmsg(telefono,Mensaje,hora,min) 

        print("Mensaje Enviado") 

    except: 

        print("Ocurrio Un Error")