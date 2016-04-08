from __future__ import absolute_import

from . import db

Puntuacion = db.Table('puntuacion',
	db.Column('id', db.Integer, primary_key=True),
	db.Column('idcliente', db.Integer, db.ForeignKey('cliente.id')),
	db.Column('iddisco', db.Integer, db.ForeignKey('disco.iddisco')),
	db.Column('puntuacion', db.Integer),
	db.Column('fecha', db.DateTime))


Discotipo = db.Table('discotipo',
	db.Column('id', db.Integer, primary_key=True),
	db.Column('iddisco', db.Integer, db.ForeignKey('disco.iddisco')),
	db.Column('idtipo', db.Integer, db.ForeignKey('tipo.idtipo')))


class Cliente(db.Model):
	__tablename__ = 'cliente'

	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(255), index=True)
	email = db.Column(db.String(255), index=True, unique=True)
	fechanacimiento = db.Column(db.DateTime)
	fecharegistro = db.Column(db.DateTime)

	score = db.relationship('Disco', secondary=Puntuacion, 
		backref=db.backref('clientes', lazy='dynamic'))

	@property
	def is_authenticated(self):
	    return True

	@property
	def is_active(self):
	    return True

	@property
	def is_anonymous():
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nombre)

        def follow(self, interprete):
            pass

        def unfollow(self, interprete):
            pass

	@staticmethod
	def make_unique_nickname(nickname):
		if not User.query.filter_by(nickname=nickname).first():
			return nickname
		version
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname


class Interprete(db.Model):
	__tablename__ = 'interprete'

	interprete = db.Column(db.String(255), index=True)
	idinterprete = db.Column(db.Integer, primary_key=True)

	discs = db.relationship('Disco', backref='interprete', lazy='dynamic')


class Disco(db.Model):
	__tablename__ = 'disco'

	id = db.Column('iddisco', db.Integer, primary_key=True)
	title = db.Column('titulo', db.String(255))
	agno = db.Column(db.Float)
	idinterprete = db.Column(db.Integer, db.ForeignKey('interprete.idinterprete'))

	genre = db.relationship('Tipo', secondary=Discotipo, 
		backref=db.backref('discos', lazy='dynamic'))


class Tipo(db.Model):
	__tablename__ = 'tipo'

	idtipo = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.String, unique=True)

        def __html__(self):
            return unicode(self.tipo)

        def __repr__(self):
            return "<{} '{}'>".format(self.__class__.__name__, self.tipo)
