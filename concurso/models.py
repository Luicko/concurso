from __future__ import absolute_import

from flask.ext.login import UserMixin

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('nombre', db.String(255), index=True)
    email = db.Column('email', db.String(255), index=True, unique=True)
    birthday = db.Column('fechanacimiento', db.DateTime)
    signindate = db.Column('fecharegistro', db.DateTime)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def follow(self, interprete):
        pass

    def unfollow(self, interprete):
        pass


class Artist(db.Model):
    __tablename__ = 'interprete'

    name = db.Column('interprete', db.String(255), index=True)
    id = db.Column('idinterprete', db.Integer, primary_key=True)

    discs = db.relationship('Song', backref='author', lazy='dynamic')


disc_type_table = db.Table('discotipo',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('iddisco', db.Integer, db.ForeignKey('disco.iddisco')),
    db.Column('idtipo', db.Integer, db.ForeignKey('tipo.idtipo')))


class Song(db.Model):
    __tablename__ = 'disco'

    id = db.Column('iddisco', db.Integer, primary_key=True)
    title = db.Column('titulo', db.String(255))
    year = db.Column('agno', db.Float)
    idart = db.Column('idinterprete',   db.Integer, db.ForeignKey('interprete.idinterprete'))

    genre = db.relationship('Genre', secondary=disc_type_table,
        backref=db.backref('discos', lazy='dynamic'))

    scores = db.relationship('Score', backref='song')

    def __repr__(self):
        return '<Disco %r>' % self.title


class Score(db.Model):
    __tablename__ = 'puntuacion'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('idcliente', db.Integer, db.ForeignKey('cliente.id'))
    song_id = db.Column('iddisco', db.Integer, db.ForeignKey('disco.iddisco'))
    score = db.Column('puntuacion', db.Integer)
    date = db.Column('fecha', db.DateTime)

    user = db.relationship('User')


class Genre(db.Model):
    __tablename__ = 'tipo'

    id = db.Column('idtipo', db.Integer, primary_key=True)
    genre = db.Column('tipo', db.String, unique=True)

    def __html__(self):
        return unicode(self.genre)

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.genre)
