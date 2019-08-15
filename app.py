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
	prodes = {}
	for p in db.session.query(Prode).all():
		prodes[p.id] = p.nombre

	return render_template('list_prodes.html', prodes=prodes)

@app.route('/prodes/<prode_id>')
def view_prode(prode_id):
	print(prode_id)
	try:
		prode_nombre = db.session.query(Prode).filter_by(id=int(prode_id)).first().nombre
		
		return render_template('view_prode.html', prode=prode_nombre, prode_id=prode_id)
	except Exception as e:
		print(e)
		return "error"

@app.route('/prodes/<prode_id>/ver_fechas')
def ver_fechas(prode_id):
	try:
		fechas_obj_list = db.session.query(Fecha).filter_by(prode_id=int(prode_id)).all()
		fechas = [x.numero for x in fechas_obj_list]
		return render_template('ver_fechas.html', prode=prode_id, fechas=fechas)
	except Exception as e:
		print(e)
		return "error"

@app.route('/prodes/<prode_id>/ver_fechas/<fecha_numero>')
def ver_fecha_numero(prode_id, fecha_numero):
	try:
		prode_nombre = db.session.query(Prode).filter_by(id=int(prode_id)).first().nombre
		
		fecha_id = db.session.query(Fecha).filter_by(prode_id=int(prode_id), numero=fecha_numero).first().id

		partidos_obj_list = db.session.query(Partido).filter_by(fecha_id=int(fecha_id)).all()
		partidos = [(x.local, x.visitante) for x in partidos_obj_list]
		
		return render_template('ver_fecha_numero.html', prode=prode_id, prode_nombre=prode_nombre, partidos=partidos, fecha_numero=fecha_numero)
	except Exception as e:
		print(e)
		return "error"

	
@app.route('/prodes/<prode_id>/agregar_fecha', methods=['GET', 'POST'])
def agregar_fecha(prode_id):
	errors = []
	prode_nombre = db.session.query(Prode).filter_by(id=int(prode_id)).first().nombre
		
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

			f = Fecha(numero, int(prode_id), partidos)
			db.session.add(f)

			db.session.commit()

		except Exception as e:
			print(e)
			errors.append("No se pudo agregar fecha a bd")
			

	return render_template('agregar_fecha.html', errors=errors, prode_nombre=prode_nombre, prode_id=prode_id)

@app.route('/prodes/<prode_id>/ver_participantes')
def ver_participantes(prode_id):
	try:
		puntos_obj_list = db.session.query(Punto).filter_by(prode_id=int(prode_id)).all()

		participantes_obj_list = []
		for p in puntos_obj_list:
			participantes_obj_list.append(db.session.query(Participante).filter_by(id=p.participante_id).first())
		

		participantes = {x.id: x.nombre for x in participantes_obj_list}
		return render_template('ver_participantes.html', prode=prode_id, participantes=participantes)
	except Exception as e:
		print(e)
		return "error"


if __name__ == '__main__':
    app.run()
