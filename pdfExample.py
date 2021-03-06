from flask import Flask, render_template, request, redirect, url_for, flash, session
from random import randint
from Conexion import conexion
from datetime import datetime, date
import time
import datetime
import os
import pymysql.cursors 

# Connection
connection = conexion()

fileName = ''
email = ''
# ###################################
# Help
def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')    



def gen_pdf_reci(id):
    return    






####################################################################################################################################
#
#      COMPROBANTE FISCAL   COMPROBANTE FISCAL    COMPROBANTE FISCAL     COMPROBANTE FISCAL
#
####################################################################################################################################

def gen_pdf_fisc(id):
    # ###################################
    # TRAIGO LOS DATOS
    cur = connection.cursor()
    data=()
    query = '''
            select empresas.*, facturas.*, factura_items.*, clientes.* , articulos.codigo
            from facturas
            left join empresas on empresas.id_empresa = facturas.id_empresa 
            left join factura_items on factura_items.id_factura = facturas.id_factura 
            left join clientes on facturas.id_cliente = clientes.id
            left join articulos on articulos.id_art = factura_items.id_art 
            where facturas.id_factura = %s
            '''
    params = [id]
    cur.execute(query,params)
    data = cur.fetchall()
    cur.close

    print(data)
    
    # CARGO LA LISTA DE DATOS
    data2 = data[0]
    
    # SACO EL MAIL DEL CLIENTE
    email = data2[65]
    if len(email) == 0:
        email = ''

    ##############################################################
    # Genero Nombre del archivo id_empresa + letra + puerto + nro
    ##############################################################
    pto = '00000'+str(data2[22])
    nro = '00000000'+str(data2[23])
    
    cdir = os.getcwd()+'/static/'
    print(cdir)
   

    fileName = cdir + str(data2[0]) +'_'+ data2[44]+pto[-5:]+'_'+nro[-8:]+'.pdf'
    fileHtml=str(data2[0]) +'_'+ data2[44]+pto[-5:]+'_'+nro[-8:]+'.pdf'


    # ###################################
    # Content
    # ###################################
    documentTitle = 'Document title!'
    title = 'Tasmanian devil'
    subTitle = 'The largest carnivorous marsupial'

    textLines = [
    'The Tasmanian devil (Sarcophilus harrisii) is',
    'a carnivorous marsupial of the family',
    'Dasyuridae.'
    ]

    image = 'afip.png'


    # ###################################
    # 0) Create document 
    # ###################################
    from reportlab.pdfgen import canvas 
    from reportlab.lib.pagesizes import A4

    pdf = canvas.Canvas(fileName ,pagesize = A4)
    pdf.setTitle(documentTitle)




    #drawMyRuler(pdf)
    # ###################################
    # 1) Title :: Set fonts 
    # # Print available fonts
    #for font in pdf.getAvailableFonts():
    #    print(font)

    # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    '''
    pdfmetrics.registerFont(
        TTFont('abc', 'SakBunderan.ttf')
    )
    pdf.setFont('abc', 36)
    pdf.drawCentredString(300, 770, title)
    '''

    #pdf.setFont('Helvetica', 18)
    #pdf.drawCentredString(300, 770, title)



    #Marco del comprobante , por omision serán de color negro
    #-line(x1,y1,x2,y2) x1,y1 inicio de line; x2, y2 fin de linea
    pdf.line(50,50,50,800)
    pdf.line(50,50,550,50)
    pdf.line(50,800,550,800)
    pdf.line(550,800,550,50)
    # RECUADRO letra del comprobante.
    pdf.line(270,800,270,760)
    pdf.line(270,760,310,760)
    pdf.line(310,760,310,800)

    pdf.line(290,760,290,700)


    pdf.setFont('Helvetica-Bold', 22)
    # letra del comprobante.
    pdf.drawCentredString(290, 780,data2[44] )
    pdf.setFont('Helvetica-Bold', 8)
    pdf.drawCentredString(282, 770,'Cod.' )
    pdf.drawCentredString(299, 770, data2[46] )

    #Empresa
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(100, 780, data2[1] )

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60, 755, 'Razón Social:')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(130, 755, data2[1])
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60, 740, 'Domicilio Comercial:')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(160, 740, data2[3])
    #Localidad
    pdf.drawString(160, 730, data2[63])
    # Condición IVA
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60, 715, 'Condición IVA: ')
    if data2[11] == 1:
        iva = 'Resp. Inscripto'
    elif  data2[11] == 2:
        iva = 'Resp. No Inscri.'
    elif  data2[11] == 3:
        iva = 'No Responsable' 
    elif  data2[11] == 4:      
        iva = 'Exento' 
    elif  data2[11] == 5:   
        iva = 'Consumidor Final'      
    elif  data2[11] == 6:   
        iva = 'Resp.Monotributo'     

    pdf.setFont('Helvetica', 9)
    pdf.drawString(135, 715, iva)

    #Cuit empresa
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(325, 735, 'CUIT: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(360, 735, data2[2])
    #Ingresos Brutos
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(325, 720, 'Ingresos Brutos: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(400, 720, data2[14]) # poner el data2[x] que corresponda

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(325, 705, 'Fecha Inicio de Actividades: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(450, 705, data2[13]) # poner el data2[x] que corresponda

    # Comprobante

    if data2[47] == 1:
        comprobante = 'FACTURA'
    elif  data2[47] == 2:
        comprobante = 'NOTA DE DEBITO'
    elif  data2[47] == 3:
        comprobante = 'NOTA DE CREDITO'
    pdf.setFont('Helvetica-Bold',12)
    pdf.drawString(325, 780, comprobante)
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(325, 765, 'Punto de Venta:')
    pto = '00000'+str(data2[22])
    nro = '00000000'+str(data2[23])
    pdf.drawString(405, 765, pto[-5:])
    pdf.drawString(440, 765, 'Nro:')
    pdf.drawString(470, 765, nro[-8:])

    #Fecha
    pdf.drawString(325, 750, 'Fecha:')
    fecha = str(data2[20]) 
    pdf.drawString(360, 750, fecha[-2:]+'/'+fecha[-5:-3]+'/'+fecha[0:4])

    # ###################################
    # 2) Sub Title 
    # RGB - Red Green and Blue
    #pdf.setFillColorRGB(0, 0, 255)
    #pdf.setFont("Courier-Bold", 24)
    #pdf.drawCentredString(290,720, subTitle)

    # ###################################
    # 3) Draw a line
    pdf.line(50, 700, 550, 700)
    pdf.line(50, 699, 550, 699)

    pdf.setFillColorRGB(0.75, 0.75, 0.75)
    #pdf.roundRect(50, 630, 500, 20, 20, stroke=1, fill=1) rectangulo con bordes redondeados
    pdf.rect(50, 630, 500, 20, stroke=1, fill=1)
    pdf.setFillColorRGB(0.00, 0.00, 0.00)


    #Código  Descripcón  Cantidad  Precio  IVA  Subtotal
    pdf.line(50, 650, 550, 650)
    pdf.setFont('Helvetica', 8)
    pdf.drawString(55,637,'Código')
    pdf.drawString(160,637,'Descripción')
    pdf.drawString(300,637,'Cantidad')
    pdf.drawString(360,637,'Precio')
    pdf.drawString(420,637,'IVA')
    pdf.drawString(480,637,'Subtotal')
    pdf.line(50, 630, 550, 630)

    # Cuit cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60, 685, 'CUIT: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(90, 685, data2[66])
    # Razón Social del cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(180, 685, 'Nombre y Apellido o Razón Social: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(332, 685, data2[63])
    # iva del cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60,670, 'Condición IVA: ')
    if data2[68] == 1:
        iva = 'Resp. Inscripto'
    elif  data2[68] == 2:
        iva = 'Resp. No Inscri.'
    elif  data2[68] == 3:
        iva = 'No Responsable' 
    elif  data2[68] == 4:      
        iva = 'Exento' 
    elif  data2[68] == 5:   
        iva = 'Consumidor Final'      
    elif  data2[68] == 6:   
        iva = 'Resp.Monotributo'     

    pdf.setFont('Helvetica', 9)
    pdf.drawString(135, 670, iva)

    #Domicilio cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(230, 670, 'Domicilio Comercial: ')
    pdf.setFont('Helvetica', 9)
    pdf.drawString(322, 670, data2[64])
    ###########################
    # Cuerpo del comprobante
    ###########################
    x = 55
    y = 620
    for row in data:
        pdf.drawString(55,y,row[72])
        pdf.drawString(100,y,row[55])
        pdf.drawRightString(320,y,str(row[59])) 
        pdf.drawRightString(380,y,str(row[57]))
        pdf.drawRightString(440,y,str(row[58]))
        pdf.drawRightString(510,y,str((row[57] + row[58])))
        y = y - 10

    ########################
    #Pie de comprobante
    ########################
    pdf.line(50, 195, 550, 195)
    pdf.line(50, 110, 550, 110)
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,180,'Neto Gravado: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,180,str(row[27]))

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,170,'IVA 27%: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,170,str(row[37]))

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,160,'IVA 21%: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,160,str(row[25]))


    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,150,'IVA 10.5%: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,150,str(row[26]))


    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,140,'IVA 0%: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,140,str(row[36]))


    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380,130,'Importe Total: $')
    pdf.setFont('Helvetica', 9)
    pdf.drawRightString(510,130,str(row[21]))

    # ###################################
    # 4) Text object :: for large amounts of text
    # from reportlab.lib import colors

    # text = pdf.beginText(40, 680)
    # text.setFont("Courier", 18)
    # text.setFillColor(colors.red)
    # for line in textLines:
    #     text.textLine(line)

    # pdf.drawText(text)


    # ###################################
    # 5) Imprimo logo afip Y CAE
    # ###################################

    pdf.setFont('Helvetica-Bold', 11)
    pdf.drawString(380,80,'CAE Nº:')
    pdf.setFont('Helvetica', 11)
    pdf.drawString(430,80,data2[28])


    #Fecha vto CAE
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(380, 70, 'Fecha de Vto. de CAE:')
    fecha = str(data2[29]) 
    pdf.setFont('Helvetica', 9)
    pdf.drawString(480, 70, fecha[-2:]+'/'+fecha[-5:-3]+'/'+fecha[0:4])

    pdf.drawString(200,70,'Comprobante Autorizado')
    pdf.drawInlineImage(image, 60,55)

    pdf.save()
    lista = [fileHtml, email]
    return lista

#gen_pdf_fisc(52)    









####################################################################################################################################
#
#      COMPROBANTE INTERNO      COMPROBANTE INTERNO      COMPROBANTE INTERNO      COMPROBANTE INTERNO      COMPROBANTE INTERNO
#
####################################################################################################################################


def gen_pdf_int(id):
    # ###################################
    # TRAIGO LOS DATOS
    cur = connection.cursor()
    data=()
    query = '''
            select empresas.*, facturas.*, factura_items.*, clientes.* , articulos.codigo
            from facturas
            left join empresas on empresas.id_empresa = facturas.id_empresa 
            left join factura_items on factura_items.id_factura = facturas.id_factura 
            left join clientes on facturas.id_cliente = clientes.id
            left join articulos on articulos.id_art = factura_items.id_art 
            where facturas.id_factura = %s
            '''
    params = [id]
    cur.execute(query,params)
    data = cur.fetchall()
    cur.close


    # CARGO LA LISTA DE DATOS
    data2 = data[0]
    
    # SACO EL MAIL DEL CLIENTE
    email = data2[65]
    if email == None:
        email = ''

    ##############################################################
    # Genero Nombre del archivo id_empresa + letra + puerto + nro
    ##############################################################
    pto = '00000'+str(data2[22])
    nro = '00000000'+str(data2[23])
    
    cdir = os.getcwd()+'/static/'

    fileName = cdir + str(data2[0]) +'_'+ data2[44]+pto[-5:]+'_'+nro[-8:]+'.pdf'
    fileHtml=str(data2[0]) +'_'+ data2[44]+pto[-5:]+'_'+nro[-8:]+'.pdf'



    # ###################################
    # 0) Create document 
    # ###################################
    from reportlab.pdfgen import canvas 
    from reportlab.lib.pagesizes import A4
    documentTitle = "Comp. Interno"

    pdf = canvas.Canvas(fileName ,pagesize = A4)
    pdf.setTitle(documentTitle)

    
    # ###################################
    # MUESTRO GRILLA
    # ###################################
    # drawMyRuler(pdf)
    
    # ###################################
    # 1) Title :: Set fonts 
    # # Print available fonts
    #for font in pdf.getAvailableFonts():
    #    print(font)

    # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics


    #Marco del comprobante , por omision serán de color negro
    #-line(x1,y1,x2,y2) x1,y1 inicio de line; x2, y2 fin de linea
    pdf.line(50,50,50,800)
    pdf.line(50,50,550,50)
    pdf.line(50,800,550,800)
    pdf.line(550,800,550,50)
    

    pdf.line(290,800,290,700)

    
    #Empresa
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(60, 760,  'COMPROBANTE INTERNO' )
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60, 740, 'Punto de Venta:')
    pto = '00000'+str(data2[22])
    nro = '00000000'+str(data2[23])
    pdf.drawString(130, 740, pto[-5:])
    pdf.drawString(160, 740, 'Nro:')
    pdf.drawString(180, 740, nro[-8:])

    #Fecha
    pdf.drawString(60, 720, 'Fecha:')
    fecha = str(data2[20]) 
    pdf.drawString(105, 720, fecha[-2:]+'/'+fecha[-5:-3]+'/'+fecha[0:4])


    # ###################################
    # 3) Draw a line
    pdf.line(50, 700, 550, 700)
    pdf.line(50, 699, 550, 699)



    pdf.setFillColorRGB(0.75, 0.75, 0.75)
    #pdf.roundRect(50, 630, 500, 20, 20, stroke=1, fill=1) rectangulo con bordes redondeados
    pdf.rect(50, 630, 500, 20, stroke=1, fill=1)
    pdf.setFillColorRGB(0.00, 0.00, 0.00)


    #Código  Descripcón  Cantidad  Precio  IVA  Subtotal
    pdf.line(50, 650, 550, 650)
    pdf.setFont('Helvetica', 8)
    pdf.drawString(55,637,'Código')
    pdf.drawString(160,637,'Descripción')
    pdf.drawString(300,637,'Cantidad')
    pdf.drawString(360,637,'Precio')
    # pdf.drawString(420,637,'IVA')
    pdf.drawString(480,637,'Subtotal')
    pdf.line(50, 630, 550, 630)

    # # Cuit cliente
    pdf.setFont('Helvetica-Bold', 9)
    if data2[19] == 0:
        pdf.drawString(60, 685, 'D.N.I: ')
        pdf.drawString(90, 685, str(data2[48]))
    else:
        pdf.drawString(60, 685, 'CUIT: ')

    pdf.setFont('Helvetica', 9)
    if data2[66] != None:
        pdf.drawString(90, 685, data2[67])
    
    # Razón Social del cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(180, 685, 'Nombre y Apellido o Razón Social: ')
    pdf.setFont('Helvetica', 9)
    if data2[49] !=None:
        pdf.drawString(332, 685, data2[49])
    
    # iva del cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(60,670, 'Condición IVA: ')
    
    iva = 'Consumidor Final'    
         
    if data2[68] == 1:
        iva = 'Resp. Inscripto'
    elif  data2[68] == 2:
        iva = 'Resp. No Inscri.'
    elif  data2[68] == 3:
        iva = 'No Responsable' 
    elif  data2[68] == 4:      
        iva = 'Exento' 
    elif  data2[68] == 5:   
        iva = 'Consumidor Final'      
    elif  data2[68] == 6:   
        iva = 'Resp.Monotributo'     

    pdf.setFont('Helvetica', 9)
    pdf.drawString(135, 670, iva)

    #Domicilio cliente
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(230, 670, 'Domicilio Comercial: ')
    pdf.setFont('Helvetica', 9)
    if data2[64] != None:
        pdf.drawString(322, 670, data2[64])

    ###########################
    # Cuerpo del comprobante
    ###########################
    x = 55
    y = 620
    for row in data:
        pdf.drawString(55,y,row[72])
        pdf.drawString(100,y,row[55])
        pdf.drawRightString(320,y,str(row[59])) 
        pdf.drawRightString(380,y,str(row[57]))
        # pdf.drawRightString(440,y,str(row[55]))
        pdf.drawRightString(510,y,str((row[57])))
        y = y - 10

    ########################
    #Pie de comprobante
    ########################
    # pdf.line(50, 155, 550, 155)
    pdf.line(50, 110, 550, 110)

    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(380,80,'Importe Total: $')
    pdf.setFont('Helvetica', 12)
    pdf.drawRightString(510,80,str(data2[21]))


    pdf.save()
    lista = [fileHtml, email]
    return lista

#gen_pdf_int(45)