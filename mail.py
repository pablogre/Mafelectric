import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail(fileName, email):

    cdir = os.getcwd() + "\static"
    print(cdir)
    # Iniciamos los parámetros del script
    remitente = 'factufacil.envios@gmail.com'
    destinatarios = [email]
    asunto = '[RPI] Correo de prueba'
    cuerpo = 'Estimado cliente le envío comprobante adjunto.'
    ruta_adjunto = cdir+'\\'+fileName
    nombre_adjunto = fileName

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; fileName= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('factufacil.envios@gmail.com','un.jinja.2020')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()  
    return    











#FUNCIONA 
#  # import necessary packages 
 
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
 
# # create message object instance
# msg = MIMEMultipart()
 
 
# message = "Thank you"
 
# # setup the parameters of the message
# password = "un.jinja.2020"
# msg['From'] = "factufacil.envios@gmail.com"
# msg['To'] = "pablogustavore@gmail.com"
# msg['Subject'] = "Subscription"
 
# # add in the message body
# msg.attach(MIMEText(message, 'plain'))
 
# #create server
# server = smtplib.SMTP('smtp.gmail.com: 587')
 
# server.starttls()
 
# # Login Credentials for sending the mail
# server.login(msg['From'], password)
 
 
# # send the message via the server.
# server.sendmail(msg['From'], msg['To'], msg.as_string())
 
# server.quit()
 
# print ("successfully sent email to %s:" % (msg['To']))











