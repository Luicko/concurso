from __future__ import absolute_import

from flask.ext.login import UserMixin

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'Cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Nombre', db.String(255), index=True)
    email = db.Column('Email', db.String(255), index=True, unique=True)
    birthday = db.Column('FechaNacimiento', db.DateTime)
    signindate = db.Column('FechaRegistro', db.DateTime)
    password = db.Column('Contrasenia', db.String(255))

    def __repr__(self):
        return '<User %r>' % (self.name)


class Artist(db.Model):
    __tablename__ = 'Interprete'

    id = db.Column('IdInterprete', db.Integer, primary_key=True)
    name = db.Column('Interprete', db.String(255), index=True)

    discs = db.relationship('Song', backref='author', lazy='dynamic')

    def __html__(self):
        return unicode(self.name)

    def __repr__(self):
        return '<Artist %r>' % self.name


disc_type_table = db.Table('DiscoTipo',
    db.Column('Id', db.Integer, primary_key=True),
    db.Column('IdDisco', db.Integer, db.ForeignKey('Disco.IdDisco')),
    db.Column('IdTipo', db.Integer, db.ForeignKey('Tipo.IdTipo')))


class Song(db.Model):
    __tablename__ = 'Disco'

    id = db.Column('IdDisco', db.Integer, primary_key=True)
    title = db.Column('Titulo', db.String(255))
    year = db.Column('Agno', db.Float)
    artist_id = db.Column('IdInterprete', db.Integer, db.ForeignKey('Interprete.IdInterprete'))

    artist = db.relationship('Artist', uselist=False)
    scores = db.relationship('Score', backref='song')
    genre = db.relationship('Genre', secondary=disc_type_table,
        backref=db.backref('Discos', lazy='dynamic'))

    def __repr__(self):
        return '<Disco %r>' % self.title


class Score(db.Model):
    __tablename__ = 'Puntuacion'

    id = db.Column('Id', db.Integer, primary_key=True)
    user_id = db.Column('Idcliente', db.Integer, db.ForeignKey('Cliente.id'))
    song_id = db.Column('Iddisco', db.Integer, db.ForeignKey('Disco.IdDisco'))
    score = db.Column('Puntuacion', db.Integer)
    date = db.Column('Fecha', db.DateTime)

    user = db.relationship('User')


class Genre(db.Model):
    __tablename__ = 'Tipo'

    id = db.Column('IdTipo', db.Integer, primary_key=True)
    genre = db.Column('Tipo', db.String, unique=True)

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.genre)