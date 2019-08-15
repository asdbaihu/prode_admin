from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/')
def home():
    return '<a href="/prodes">prodes<a><br><a href="/crear_prode">crear prode<a>'

@app.route('/crear_prode', methods=['GET', 'POST'])
def crear_prode():
	errors = []
	if request.method == "POST": 
		try:
			nombre = request.form['nombre']
			#print(nombre)
			#pr = request.get(nombre)
			#participante1 = request.form['participante1']
			cantidad_participantes = request.form['cantidad']

			participantes = []
			for i in range(int(cantidad_participantes)):
				participantes.append(request.form['participante' + str(i+1)])
			
		except Exception as e:
			print(e)
			errors.append("unable to ")
			return render_template('agregar_prode.html', errors=errors)


		if nombre:
			try:
				#print(nombre)
				p = Prode(nombre)
				db.session.add(p)
				print(p.id)
				db.session.commit()
				#part = Participante(participante1, db.session.filter_by(nombre=nombre).all().id)
				
				new_id = db.session.query(Prode).order_by(Prode.id.desc()).first().id 
				#print(participante1)
				
				#part = Participante(participante1, new_id)
				
				parts_objs = [Participante(p, new_id) for p in participantes]

				db.session.add_all(parts_objs)
				db.session.commit()
			except Exception as e:
				print(e)
				errors.append("Unable to add to database")

		
	return render_template('agregar_prode.html', errors=errors)



@app.route('/prodes')
def list_prodes():
	prodes = []
	for p in db.session.query(Prode).all():
		prodes.append(p.nombre)

	return render_template('list_prodes.html', prodes=prodes)

@app.route('/prodes/<prode>')
def view_prode(prode):
	print(prode)
	return render_template('view_prode.html', prode=prode)

@app.route('/prodes/<prode>/ver_fechas')
def ver_fechas(prode):


@app.route('/prodes/<prode>/agregar_fecha', methods=['GET', 'POST'])
def agregar_fecha(prode):
	errors = []
	if request.method == "POST": 
		try:
			cantidad_equipos = request.form['cantidad']
			cantidad_equipos = (int(cantidad_equipos)*2)
			numero = request.form['numero']
			equipos = []
			for i in range(1, cantidad_equipos+1):
				equipos.append(request.form['equipo' + str(i)])
		except Exception as e:
			print(e)
			errors.append("unable to ")
			return render_template('agregar_fecha.html', errors=errors)

		try:
			id_new_f = db.session.query(Fecha).order_by(Fecha.id.desc()).first().id + 1

			print(id_new_f)
				
			partidos = []
			#fecha_id, local, visitante
			for i in range(0, len(equipos), 2):
				partidos.append(Partido(id_new_f, equipos[i], equipos[i+1]))
			
			db.session.add_all(partidos)
				

			for p in partidos:
				db.session.add(p)

			f = Fecha(numero, 1, partidos)
			db.session.add(f)

			db.session.commit()

		except Exception as e:
			print(e)
			errors.append("No se pudo agregar fecha a bd")
			

	return render_template('agregar_fecha.html', errors=errors, prode=prode)


if __name__ == '__main__':
    app.run()
