import datetime
import csv

from flask import render_template, redirect, url_for, request, g, flash, request
from flask.ext.login import (login_user, logout_user, current_user,
    login_required
    )
from sqlalchemy import select

from . import app, db, lm
from . import utils
from .models import *
from .forms import Regist_Form, Login_Form


@app.route('/')
@app.route('/index')
def index():
	import random
	news = Songs.query.all()
	random.shuffle(news)
	slide = news[0:7]
	if current_user.is_authenticated:
		follow_list = read_follow()
	else:
		follow_list = []
	artist_list = Artist.query.all()
	return render_template('index.html', title='Main',
		news=news, slide=slide, follow_list=follow_list, artist_list=artist_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user is not None and current_user.is_authenticated:
		return redirect(url_for('index'))
	form = Login_Form()
	if form.validate_on_submit():
		u = User.query.filter_by(email=form.email.data).first()
		if not u:
			flash('Error al iniciar sesion')
			return redirect(url_for('login'))
		else:
			login_user(u)
			return redirect(url_for('index'))
	return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = Regist_Form()
	if current_user is not None and current_user.is_authenticated:
		return redirect(url_for('index'))
	form = Regist_Form()
	if form.validate_on_submit():
		u = User(email=form.email.data, name=form.nickname.data, 
			signindate=datetime.datetime.utcnow(), birthday=form.birthday.data)
		db.session.add(u)
		db.session.commit()
		flash('Welcome!')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form, title='Join')


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/artist')
def artists():
	artist_list = Artist.query.all()
	return render_template('artists.html', artist_list=artist_list)


@app.route('/songs')
def songs():
	song_list = Songs.query.all()
	genre_list = Genre.query.all()
	artist_list = Artist.query.all()
	return render_template('songs.html', song_list=song_list, genre_list=genre_list)


@app.route('/songs/<id>/<songs>')
def song(id, songs):
	act_song = Songs.query.filter_by(id=id).first()
	year = int(act_song.year)
	if current_user.is_authenticated:
		if act_song in current_user.score:
			select = select([Puntuacion.c.puntuacion]).where(Puntuacion.c.idcliente == current_user.id)\
			.where(Puntuacion.c.iddisco==act_song.id)
			result = db.session.execute(final)
			for row in result:
				score = row[0]
		else:
			score = 100
	score = 100
	return render_template('song.html', title=act_song.title, act_song=act_song,
		year=year, score=score)


@app.route('/set_score', methods=['GET', 'POST'])
def set_score():
	score = request.form.get('rating')
	song = request.form.get('song')
	##FALTA REVISION
	exe = Puntuacion.insert().values(iddisco=song, puntuacion=score,
			idcliente=current_user.id,
			fecha=datetime.datetime.utcnow())
	db.session.execute(exe)
	db.session.commit()
	return 'Done'


@app.route('/follow', methods=['GET','POST'])
def follow(artist):
	follow_file = open('.static/following/',usuario.id,'.csv','a')
	follow_file.write("",artist.id," ")
	follow_file.close()


@app.route('/unfollow', methods=['GET', 'POST'])
def unfollow(artist):
	following = read_follow(usuario)
	following.remove(str(artist))
	os.remove('',usuario.id,'.csv')
	follow_file = open('.static/following/',usuario.id,'.csv','a')
	for x in range(len(following)):
		follow_file.write("",following[x]," ")
	follow_file.close()
	return 'Done'


def read_follow():
	follow = []
	try:
		with open('.static/following/'+str(current_user.id)+'.csv', 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ')
			for row in spamreader:
				follow = row
		return follow
	except IOError:
		return follow
