from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import *

class PartidoSchema(ma.Schema):
	class Meta:
		fields = ['id', 'fecha_id', 'local', 'visitante', 'resultado', 'punto_personalizado', 'pleno_personalizado']

class FechaSchema(ma.Schema):
	partidos = ma.Nested(PartidoSchema, many=True)
	class Meta:
		fields = ['id', 'prode_id', 'numero', 'partidos']

class ProdeSchema(ma.Schema):
	fechas = ma.Nested(FechaSchema, many=True)
	class Meta:
		fields = ['id', 'nombre', 'fechas']

class PronosticoSchema(ma.Schema):
	class Meta:
		fields = ['participante_id', 'partido_id', 'resultado']

class ParticipanteSchema(ma.Schema):
	pronosticos = ma.Nested(PronosticoSchema, many=True)
	class Meta:
		fields = ['id', 'nombre', 'puntos', 'plenos', 'pronosticos']


prode_schema = ProdeSchema(strict=True)
prodes_schema = ProdeSchema(many=True, strict=True)

partido_schema = PartidoSchema(strict=True)
partidos_schema = PartidoSchema(many=True, strict=True)

fecha_schema = FechaSchema(strict=True)
fechas_schema = FechaSchema(many=True, strict=True)

pronostico_schema = PronosticoSchema(strict=True)
pronosticos_schema = PronosticoSchema(many=True, strict=True)

participante_schema = ParticipanteSchema(strict=True)
participantes_schema = ParticipanteSchema(many=True, strict=True)

@app.route('/')
def hello():
	return "Hi"

#----------------------#

#Prode methods

#----------------------#

@app.route('/api/prode', methods=['POST'])
def agregar_prode():
	if request.method == "POST":
		nombre = request.json['nombre']
		print(nombre)

		nuevo_prode = Prode(nombre)

		db.session.add(nuevo_prode)
		db.session.commit()

		return prode_schema.jsonify(nuevo_prode)

@app.route('/api/prode', methods=['GET'])
def get_prode():
	if request.method == "GET":
		todos = Prode.query.all()
		r = prodes_schema.dump(todos)

		return jsonify(r.data)

@app.route('/api/prode/<id>', methods=['GET'])
def get_prode_by_id(id):
	if request.method == "GET":
		prode = Prode.query.get(id)
		return prode_schema.jsonify(prode)

@app.route('/api/prode/<id>', methods=['PUT'])
def actualizar_prode(id):
	if request.method == "PUT":
		prode = Prode.query.get(id)
		
		nombre = request.json['nombre']

		prode.nombre = nombre
		
		db.session.commit()

		return prode_schema.jsonify(prode)

@app.route('/api/prode/<id>', methods=['DELETE'])
def eliminar_prode(id):
	if request.method == "DELETE":
		prode = Prode.query.get(id)

		db.session.delete(prode)
		db.session.commit()

		return prode_schema.jsonify(prode)

#----------------------#

#Participante methods

#----------------------#

@app.route('/api/participante', methods=['POST'])
def agregar_participante():
	if request.method == "POST":
		nombre = request.json['nombre']
		prode_id = request.json['prode_id']

		nuevo_participante = Participante(nombre, prode_id)

		db.session.add(nuevo_participante)
		db.session.commit()

		return prode_schema.jsonify(nuevo_participante)

@app.route('/api/participante', methods=['GET'])
def get_participante():
	if request.method == "GET":
		todos = Participante.query.all()
		r = participantes_schema.dump(todos)

		return jsonify(r.data)

@app.route('/api/participante/<id>', methods=['GET'])
def get_participante_by_id(id):
	if request.method == "GET":
		participante = Participante.query.get(id)
		return participante_schema.jsonify(participante)

@app.route('/api/participante/<id>', methods=['PUT'])
def actualizar_participante(id):
	if request.method == "PUT":
		participante = Participante.query.get(id)
		
		nombre = request.json['nombre']
		prode_id = request.json['prode_id']

		participante.nombre = nombre
		participante.prode_id = prode_id
		
		db.session.commit()

		return participante_schema.jsonify(participante)

@app.route('/api/participante/<id>', methods=['DELETE'])
def eliminar_participante(id):
	if request.method == "DELETE":
		participante = Participante.query.get(id)

		db.session.delete(participante)
		db.session.commit()

		return participante_schema.jsonify(participante)

#----------------------#

#Fecha methods

#----------------------#
    
@app.route('/api/fecha', methods=['POST'])
def agregar_fecha():
	if request.method == "POST":
		numero = request.json['numero']
		prode_id = request.json['prode_id']

		nueva_fecha = Fecha(numero, prode_id)

		db.session.add(nueva_fecha)
		db.session.commit()

		return fecha_schema.jsonify(nueva_fecha)

@app.route('/api/fecha', methods=['GET'])
def get_fecha():
	if request.method == "GET":
		todos = Fecha.query.all()
		r = fechas_schema.dump(todos)

		return jsonify(r.data)

@app.route('/api/fecha/<id>', methods=['GET'])
def get_fecha_by_id(id):
	if request.method == "GET":
		fecha = Fecha.query.get(id)
		return fecha_schema.jsonify(fecha)

@app.route('/api/fecha/<id>', methods=['PUT'])
def actualizar_fecha(id):
	if request.method == "PUT":
		fecha = Fecha.query.get(id)
		
		numero = request.json['numero']
		prode_id = request.json['prode_id']

		fecha.numero = numero
		fecha.prode_id = prode_id
		
		db.session.commit()

		return fecha_schema.jsonify(fecha)

@app.route('/api/fecha/<id>', methods=['DELETE'])
def eliminar_fecha(id):
	if request.method == "DELETE":
		fecha = Fecha.query.get(id)

		db.session.delete(fecha)
		db.session.commit()

		return fecha_schema.jsonify(fecha)

#----------------------#

#Partido methods

#----------------------#

@app.route('/api/partido', methods=['POST'])
def agregar_partido():
	if request.method == "POST":
		fecha_id = request.json['fecha_id']
		local = request.json['local']
		visitante = request.json['visitante']

		if(request.json['personalizado']):
			punto_personalizado = request.json['punto_personalizado']
			pleno_personalizado = request.json['pleno_personalizado']
		else:
			punto_personalizado = None
			pleno_personalizado = None

		nuevo_partido = Partido(fecha_id, local, visitante, None, punto_personalizado, pleno_personalizado)

		db.session.add(nuevo_partido)
		db.session.commit()

		return partido_schema.jsonify(nuevo_partido)

@app.route('/api/partido', methods=['GET'])
def get_partido():
	if request.method == "GET":
		todos = Partido.query.all()
		r = partidos_schema.dump(todos)

		return jsonify(r.data)

@app.route('/api/partido/<id>', methods=['GET'])
def get_partido_by_id(id):
	if request.method == "GET":
		partido = Partido.query.get(id)
		return partido_schema.jsonify(partido)

@app.route('/api/partido/<id>', methods=['PUT'])
def actualizar_partido(id):
	if request.method == "PUT":
		partido = Partido.query.get(id)
		
		fecha_id = request.json['fecha_id']
		local = request.json['local']
		visitante = request.json['visitante']

		if(request.json['personalizado']):
			punto_personalizado = request.json['punto_personalizado']
			pleno_personalizado = request.json['pleno_personalizado']
		else:
			punto_personalizado = None
			pleno_personalizado = None

		partido.fecha_id = fecha_id
		partido.local = local
		partido.punto_personalizado = punto_personalizado
		partido.pleno_personalizado = pleno_personalizado

		db.session.commit()

		return partido_schema.jsonify(partido)

@app.route('/api/partido/<id>', methods=['DELETE'])
def eliminar_partido(id):
	if request.method == "DELETE":
		partido = Partido.query.get(id)

		db.session.delete(partido)
		db.session.commit()

		return partido_schema.jsonify(partido)

#----------------------#

#Pronostico methods

#----------------------#

@app.route('/api/pronostico', methods=['POST'])
def agregar_pronostico():
	if request.method == "POST":

		participante_id = request.json['participante_id']
		partido_id = request.json['partido_id']
		resultado = request.json['resultado']

		nuevo_pronostico = Pronostico(participante_id, partido_id, resultado)

		db.session.add(nuevo_pronostico)
		db.session.commit()

		return pronostico_schema.jsonify(nuevo_pronostico)

@app.route('/api/pronostico', methods=['GET'])
def get_pronostico():
	if request.method == "GET":
		todos = Pronostico.query.all()
		r = pronosticos_schema.dump(todos)

		return jsonify(r.data)

@app.route('/api/pronostico/<id>', methods=['GET'])
def get_pronostico_by_id(id):
	if request.method == "GET":
		pronostico = Pronostico.query.get(id)
		return pronostico_schema.jsonify(pronostico)

@app.route('/api/pronostico/<id>', methods=['PUT'])
def actualizar_pronostico(id):
	if request.method == "PUT":
		pronostico = Pronostico.query.get(id)
		
		participante_id = request.json['participante_id']
		partido_id = request.json['partido_id']
		resultado = request.json['resultado']

		pronostico.participante_id = participante_id
		pronostico.partido_id = partido_id
		pronostico.resultado = resultado

		db.session.commit()

		return pronostico_schema.jsonify(pronostico)

@app.route('/api/pronostico/<id>', methods=['DELETE'])
def eliminar_pronostico(id):
	if request.method == "DELETE":
		pronostico = Pronostico.query.get(id)

		db.session.delete(pronostico)
		db.session.commit()

		return pronostico_schema.jsonify(pronostico)

 ######
# html #
 ######

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/prodes')
def prodes():
	return render_template('prodes.html')




if __name__ == '__main__':
	app.run()