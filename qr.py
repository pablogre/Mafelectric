from flask import Flask, render_template, request, redirect, url_for, flash, session
from Conexion import conexion 
from random import randint
from datetime import datetime, date
import time
import datetime
import os
import pymysql.cursors 
import qrcode
import json
import base64



connection=conexion()

def qr(id):
    #id de la factura
    print('id de la fact.:',id)
    # Connection
    connection = conexion()
    query = '''
        SELECT f.fecha,e.cuit,f.puerto,f.cod_afip,f.numero,f.total,f.dni,f.cae
		from facturas f,empresas e
        WHERE  e.id_empresa=f.id_empresa and f.id_factura=%s 
        '''
    cur = connection.cursor()
    #data=()
    params = [id]
    cur.execute(query,params)
    data = cur.fetchall()
    cur.close
    connection.close()

    print('DATA:',data)

    data2 = data[0]
	#DNI
    if data2[6] > 20000000000 :
        tipodoc='80'  
		#80 cuit
    else :
        tipodoc='96'    	
    # CARGO LA LISTA DE DATOS

    fecha = str(data2[0])
    fFecha = fecha[8:10] +'/'+fecha[5:7]+'/'+fecha[0:4]

    qr={
	# ver	Numérico 1 digito	OBLIGATORIO – versión del formato de los datos del comprobante	1
    "ver":'1',
	#fecha	full-date (RFC3339)	OBLIGATORIO – Fecha de emisión del comprobante	"2020-10-13"  
    "fecha":fFecha,
	#cuit	Numérico 11 dígitos	OBLIGATORIO – Cuit del Emisor del comprobante	30000000007
    "cuit":data2[1],
	#ptoVta	Numérico hasta 5 digitos	OBLIGATORIO – Punto de venta utilizado para emitir el comprobante	10
    "ptoVta":str(data2[2]),
	#tipoCmp	Numérico hasta 3 dígitos	OBLIGATORIO – tipo de comprobante (según Tablas del sistema )	1
    "tipoCmp":str(data2[3]),
	#nroCmp	Numérico hasta 8 dígitos	OBLIGATORIO – Número del comprobante	94
    "nroCmp":str(data2[4]),
	#importe	Decimal hasta 13 enteros y 2 decimales	OBLIGATORIO – Importe Total del comprobante (en la moneda en la que fue emitido)	12100
    "importe":str(data2[5]),
	#moneda	3 caracteres	OBLIGATORIO – Moneda del comprobante (según Tablas del sistema )	"DOL"
    "moneda":"PES",
	#ctz	Decimal hasta 13 enteros y 6 decimales	OBLIGATORIO – Cotización en pesos argentinos de la moneda utilizada (1 cuando la moneda sea pesos)	65
    "ctz":'1.00',
	#tipoDocRec	Numérico hasta 2 dígitos	DE CORRESPONDER – Código del Tipo de documento del receptor (según Tablas del sistema )	80
    "tipoDocRec":tipodoc,
	#nroDocRec	Numérico hasta 20 dígitos	DE CORRESPONDER – Número de documento del receptor correspondiente al tipo de documento indicado	20000000001
    "nroDocRec":data2[6],
	#tipoCodAut	string	OBLIGATORIO – “A” para comprobante autorizado por CAEA, “E” para comprobante autorizado por CAE	"E"
    "tipoCodAut":"E",
	#codAut	Numérico 14 dígitos	OBLIGATORIO – Código de autorización otorgado por AFIP para el comprobante	70417054367476   
	"codAut":data2[7]
	}
    ### GENERO JSON
    cStringQrjson = json.dumps(qr)

    ### LO PASO A BASE64
    lcString64 = base64.b64encode(cStringQrjson.encode("utf-8"))

    ### GENERO LA IMAGEN QR
    pcQR = 'https://www.afip.gob.ar/fe/qr/?p=' + str(lcString64)
    cdir = os.getcwd()+'/static/images/'
    img = qrcode.make(pcQR)
    f = open(cdir+"qr.png", "wb")
    img.save(f)
    f.close()
    qrimage = cdir+'qr.png'
    return qrimage
   
  

