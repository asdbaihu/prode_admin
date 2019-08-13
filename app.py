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
    return render_template('view_prode.html', prode=prode)


if __name__ == '__main__':
    app.run()
