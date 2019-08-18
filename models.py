from app import db
from flask_marshmallow import Marshmallow

class Prode(db.Model):
    __tablename__ = 'prodes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    fechas = db.relationship("Fecha", backref='prodes')
    participantes =  db.relationship("Participante", backref='prodes')

    def __init__(self, nombre):
        self.nombre = nombre

class Participante(db.Model):
    __tablename__ = 'participantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    pronosticos = db.relationship("Pronostico", backref='participantes')
    prode_id = db.Column(db.Integer, db.ForeignKey('prodes.id'),
        nullable=False)

    puntos = db.Column(db.Integer)
    plenos = db.Column(db.Integer)

    def __init__(self, nombre, prode_id):
        self.nombre = nombre
        self.prode_id = prode_id
        self.puntos = 0
        self.plenos = 0

class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)

    fecha_id = db.Column(db.Integer, db.ForeignKey('fechas.id'),
        nullable=False)

    punto_personalizado = db.Column(db.Float, nullable=True)
    pleno_personalizado = db.Column(db.Float, nullable=True)

    local = db.Column(db.String())
    visitante = db.Column(db.String())
    resultado = db.Column(db.String(), nullable=True)


    def __init__(self, fecha_id, local, visitante, resultado=None, punto_personalizado=None, pleno_personalizado=None):
        self.fecha_id = fecha_id
        self.local = local
        self.visitante = visitante
        self.resultado = resultado
        self.punto_personalizado = punto_personalizado
        self.pleno_personalizado = pleno_personalizado


class Fecha(db.Model):
    __tablename__ = 'fechas'

    id = db.Column(db.Integer, primary_key=True)

    prode_id = db.Column(db.Integer, db.ForeignKey('prodes.id'),
        nullable=False)

    numero = db.Column(db.Integer)

    partidos = db.relationship("Partido", backref='fechas')

    def __init__(self, numero, prode_id):
        self.numero = numero
        self.prode_id = prode_id


class Pronostico(db.Model):
    __tablename__ = 'pronosticos'

    id = db.Column(db.Integer, primary_key=True)

    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id'),
        nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'),
        nullable=False)

    resultado = db.Column(db.String())

    def __init__(self, participante_id, partido_id, resultado):
        self.participante_id = participante_id
        self.partido_id = partido_id
        self.resultado = resultado 


