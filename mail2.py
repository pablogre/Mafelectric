
import smtplib

def mailme():
    SERVER_NAME='smtp.gmail.com'
    SERVER_PORT=587
    USER_NAME='factufacil.envios@gmail.com'
    PASSWORD='un.jinja.2020'
    print('connecting')
    server = smtplib.SMTP(SERVER_NAME, SERVER_PORT)
    print('connected..')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(USER_NAME, PASSWORD)
    text = 'TEST 123'
    server.sendmail('factufacil.envios@gmail.com', 'pablogustavore@gmail.com', text)
    server.quit()
    return

mailme()



'''
import os
import smtplib

from_addr = 'factufacil.envios@gmail.com'
to = 'pablogustavore@gmail.com'

message = 'prueba de un jinja'

username = 'factufacil.envios@gmail.com'
password = 'un.jinja.2020'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(from_addr, to, message)

server.quit()
'''