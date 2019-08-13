from app import db


'''class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)'''

class Prode(db.Model):
    __tablename__ = 'prodes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    fechas = db.relationship("Fecha", backref='prodes')

    def __init__(self, nombre):
        self.nombre = nombre


class Participante(db.Model):
    __tablename__ = 'participantes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    puntos = db.relationship("Punto", backref='participantes')
    pronosticos = db.relationship("Pronostico", backref='participantes')

    def __init__(self, nombre, prode_id):
        self.nombre = nombre
        self.puntos = [Punto(prode_id, id)]


class Punto(db.Model):
    __tablename__ = 'puntos'

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    plenos = db.Column(db.Integer)

    prode_id = db.Column(db.Integer, db.ForeignKey('prodes.id'),
        nullable=False)
    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id'),
        nullable=False)

    def __init__(self, prode_id, participante_id):
        self.cantidad = 0
        self.plenos = 0

        self.prode_id = prode_id
        self.participante_id = participante_id

class Partido(db.Model):
    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)

    fecha_id = db.Column(db.Integer, db.ForeignKey('fechas.id'),
        nullable=False)

    local = db.Column(db.String())
    visitante = db.Column(db.String())
    resultado = db.Column(db.String())

class Fecha(db.Model):
    __tablename__ = 'fechas'

    id = db.Column(db.Integer, primary_key=True)

    prode_id = db.Column(db.Integer, db.ForeignKey('prodes.id'),
        nullable=False)

    cantidad = db.Column(db.Integer)

    partidos = db.relationship("Partido", backref='fechas')


class Pronostico(db.Model):
    __tablename__ = 'pronosticos'

    id = db.Column(db.Integer, primary_key=True)

    participante_id = db.Column(db.Integer, db.ForeignKey('participantes.id'),
        nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'),
        nullable=False)

    resultado = db.Column(db.String())
