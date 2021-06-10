import pymysql.cursors 

def conexion():
    c = pymysql.connect(host='138.36.236.45' ,
                             user= 'root', 
                             password= 'kagupuVU87', 
                             db= 'gestion',
                             #db= 'sqldata',
                             charset='utf8mb4'
                             )
    return c	

def sql(query,params):
    connection = conexion()
    cur = connection.cursor()
    sql = query 
    cur.execute(sql,params)
    data = cur.fetchall()
    cur.close()
    connection.close()
    return data

