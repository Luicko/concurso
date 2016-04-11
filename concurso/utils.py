import csv

from . import app, db
from .models import User, Songs, Artist


def follow(Artist, usuario):
	follow_file = open('/following/',usuario.id,'.csv','a')
	follow_file.write("",Artist.id," ")
	follow_file.close()

def unfollow(usuario, Artist):
	following = read_follow(usuario)
	following.remove(str(Artist))
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

def set_score(user, score, disc):
	x = models.Puntuacion.query.filter(idUser=user.id, idSongs=disc.id).first()
	if x:
		j = x(Puntuacion=score)
		db.session.add(j)
		db.session.commit()
	else:
		x = models.Puntuacion(idUser=user.id, idSongs=disc.id, puntuacion=score)
		db.session.add(x)
		db.session.commit()