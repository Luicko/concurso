import datetime

from flask import render_template, redirect, url_for, request, g, flash
from flask.ext.login import (login_user, logout_user, current_user,
    login_required
    )

from . import app, db, lm
from . import utils
from .models import Cliente, Disco, Interprete
from .forms import Regist_Form, Login_Form


@app.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
	return Cliente.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	import random
	user = g.user
	news = utils.all_discs()
	random.shuffle(news)
	slide = news[0:7]
	return render_template('index.html', title='Main', user=user, 
		news=news, slide=slide)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = Login_Form()
	if form.validate_on_submit():
		u = Cliente.query.filter_by(email=form.email.data).first()
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
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = Regist_Form()
	if form.validate_on_submit():
		u = Cliente(email=form.email.data, nombre=form.nickname.data, 
			fecharegistro=datetime.datetime.utcnow(), fechanacimiento=form.birthday.data)
		db.session.add(u)
		db.session.commit()
		flash('Welcome!')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form, title='Join')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/interprete')
def interpretes():
	inter_list = utils.all_inter()
	return render_template('interprete.html', inter_list=inter_list)

@app.route('/inter/<interprete>')
def inter(interprete):
	act_inter = utils.one_inter(interprete)
	return render_template('inter.html', title=act_inter.interprete,
	 act_inter=act_inter)
	
@app.route('/user/<user>')
def test(usuario):
	follow = read_follow(usuario)
	following = select_follow(x)
	usu = usuario
	return render_template('usuario.html', title=usu.nickname, 
		following=following, usu=usu)

@app.route('/discos')
def discos():
	disc_list = utils.all_discs
	return render_template('discos.html', disc_list=disc_list)

@app.route('/disc/<discos>')
def disc(discos):
	name = disco.titulo
	act_disc = utils.one_disc(disco)
	return render_template('disc.html', title=act_disc.titulo, act_disc=act_disc)

@app.route('/score', methods=['GET', 'POST'])
def score(points, disco):
	user = g.user
	utils.set_score(user=user, score=points, disc=disco)
	pass
