import csv

from . import app, db
from .models import Cliente, Disco, Interprete


def follow(interprete, usuario):
	follow_file = open('/following/',usuario.id,'.csv','a')
	follow_file.write("",interprete.id," ")
	follow_file.close()

def unfollow(usuario, interprete):
	following = read_follow(usuario)
	following.remove(str(interprete))
	os.remove('',usuario.id,'.csv')
	follow_file = open('/following/',usuario.id,'.csv','a')
	for x in range(len(following)):
		follow_file.write("",following[x]," ")
	follow_file.close()


def read_follow(usuario):
	follow = []
	try:
		with open('/following/',usuario.id,'.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter= ' ')
			for row in spamreader:
				follow = row
		return follow
	except IOError:
		return None


def select_follow(fal):
	select = []
	for x in range(len(fal)):
		select.append(Interprete.query.filter_by(id=int(fal[x])).first())
	return select

def all_inter():
	inter = Interprete
	select = inter.query.all()
	return select

def all_discs():
	disc = Disco
	select = disc.query.all()
	return select

def one_inter(interprete):
	inter = Interprete
	select = inter.query.filter_by(idinterprete=interprete).first()
	return select

def one_disc(disco):
	disc = Disco
	select = disc.query.filter_by(iddisco=disco).first()
	return select

def set_score(user, score, disc):
	x = models.Puntuacion.query.filter(idcliente=user.id, iddisco=disc.id).first()
	if x:
		j = x(Puntuacion=score)
		db.session.add(j)
		db.session.commit()
	else:
		x = models.Puntuacion(idcliente=user.id, iddisco=disc.id, puntuacion=score)
		db.session.add(x)
		db.session.commit()
