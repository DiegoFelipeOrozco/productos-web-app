from flask import Flask, request, render_template, url_for
import requests

API_ADDRESS = 'http://127.0.0.1:5000'
TIPOS = ['Flor','Grano','Verdura', 'Fruta', 'Hortaliza']

app = Flask(__name__)


@app.route('/lista_productos',methods=['GET'])
def listarProductos():
	return render_template('productoList.html', productos=cleanDataResponse(requests.get(API_ADDRESS+'/productos').json()))

@app.route('/form_crear',methods=['GET'])
def crearProducto():
	return render_template('productoForm.html', tipos=TIPOS, icono=url_for('static', filename='Evergreen.jpeg'))

@app.route('/crear_producto',methods=['POST'])
def guardarProducto():
	requests.post(API_ADDRESS+'/productos', json=cleanDataRequest(request.form))
	return listarProductos()

def cleanDataRequest(requestDict):
	dataRequest = dict(requestDict)
	if (dataRequest["caducidad"] == ''):
		del(dataRequest["caducidad"])

	if (dataRequest["imagen"] == ''):
		del(dataRequest["imagen"])
	return dataRequest

def cleanDataResponse(responseDict):
	for producto in responseDict:
		if (producto["Periodo_caducidad"] == None):
			producto["Periodo_caducidad"] = ''

		if (producto["Imagen"] == None):
			producto["Imagen"] = 'https://luzevergreen.files.wordpress.com/2016/03/fondo.jpg?w=604&h=270&crop=1'
	return responseDict

if __name__=="__main__":
	app.run(port=8000,debug=True)