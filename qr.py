import qrcode
url = 'http://192.168.0.114:5000/ver_trabajos?estado=null&id_ot=102'
qr = qrcode.QRCode(version = 1, box_size=10,border=1)
qr.add_data(url)
qr.make(fit=True)

img=qr.make_image(fill='black', back_color='white')
img.save('.\static\qr_102.png')