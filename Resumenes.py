from flask import Blueprint,Flask, render_template, request, redirect, url_for, flash, session
resumenes = Blueprint('resumenes', __name__)
from Conexion import conexion 
from random import randint
from datetime import datetime, date
import time
import datetime
import os
import pymysql.cursors 

# Connection
connection=conexion()
#This is the index route where we are going to
#query on all our employee data
def estoy():
    if not session.get('id_empresa'):
        return render_template('login.html')
		
################################################## NICO

@resumenes.route('/iva_ventas/', methods = ['GET','POST'])
def iva_ventas():
    estoy()
    d=datetime.date.today()
    vyear = d.year
    vmonth = d.month
    tipo=''		
    if request.method == 'POST':
        vmonth = request.form['mes']
        vyear = request.form['anio']
        tipo = request.form['informe']
    id_empresa = session['id_empresa']
    cur = connection.cursor()    
    if tipo=='resumen':
        #Resumen Por Tipo de IVa
        query = '''SELECT sum(excento) ,sum(iva21), sum(neto21) ,sum(iva105), 
        sum(neto105),sum(iva27) , sum(neto27) ,sum(iva0),sum(neto0),sum(total) 
        FROM `facturas` WHERE  cod_afip > 0 and id_empresa=%s and month(facturas.fecha)=%s and year(facturas.fecha)=%s'''
        params = [id_empresa,vmonth,vyear]
        cur.execute(query, params)
        data1=cur.fetchall()        
        return render_template('resumenes/iva_ventas_resumen.html',anio=vyear,mes=vmonth,resumen=data1)
    if tipo=='detalle':
        #Detalle de Facturas
        query = '''SELECT c.cuit,c.cliente,f.excento,f.iva,f.neto,f.total
        FROM facturas f , clientes c WHERE f.id_empresa=%s 
		and f.id_cliente=c.id and cod_afip > 0
		and month(f.fecha)=%s and year(f.fecha)=%s'''
        params = [id_empresa,vmonth,vyear] 
        cur.execute(query, params)
        data2=cur.fetchall()
        cur.close()
        print(query,data2)
        return render_template('resumenes/iva_ventas_detalle.html',anio=vyear,mes=vmonth,detalle=data2)	
    if tipo=='':
        return render_template('resumenes/iva_ventas.html',anio=vyear,mes=vmonth)

@resumenes.route('/citi_ventas/', methods = ['GET','POST'])
def citi_ventas():
    '''id_empresa = session['id_empresa']
    usuario = session['id_usuario']
    cur = connection.cursor()
    query = "update factura_tmp set estado = 'E' where id_empresa = %s and usuario = %s"
    params = [id_empresa, usuario]
    cur.execute(query, params)
    connection.commit()
    cur.close()'''
    return render_template('resumenes/citi_ventas.html')
	
@resumenes.route('/ingresos_ventas/', methods = ['GET','POST'])
def ingresos_ventas():
    estoy()
    id_empresa = session['id_empresa']
    tipo=0
    dias=0
    if request.method == 'POST':
        tipo=request.form['tipo']
        dias=request.form['dias']
    cur = connection.cursor()
      		
    
    
    query = '''
            select clientes.id,clientes.cliente,T1.*from (
            select facturas.fecha ,
            concat(CASE WHEN facturas.id_tipo_comp = 1 THEN 'FC '
            WHEN facturas.id_tipo_comp = 2 THEN 'NC '
            WHEN facturas.id_tipo_comp = 3 THEN 'ND '
            END  ,  facturas.letra,' ',lpad(facturas.puerto,5,'0'),'-',lpad(facturas.numero,8,'0')) as nro,
            facturas_mpagos.importe, facturas.id_factura,facturas.id_cliente,facturas.id_empresa
            from facturas_mpagos 
            left join facturas on facturas.id_factura = facturas_mpagos.id_factura 
            left join clientes on clientes.id = facturas.id_cliente
            UNION 
            select recibos.fecha, concat('REC ','00001-',lpad(recibos.numero,8,'0')), recibos.total * -1,
            recibos.id ,recibos.id_cliente,recibos.id_empresa
            from recibos ) as T1, clientes
            where T1.id_cliente = clientes.id and T1.fecha BETWEEN %s and %s and T1.id_empresa = %s
            order by T1.fecha
            '''
    params = [id_empresa]
    #cur.execute(query, params)
    #connection.commit()
    cur.close()
    if tipo==0:
        return render_template('resumenes/ingresos_ventas.html')
    else:
        return render_template('resumenes/ingresos_tipos.html')                	
