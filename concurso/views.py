import datetime
import csv

from flask import render_template, redirect, url_for, flash, request, jsonify, g
from flask.ext.login import (login_user, logout_user, current_user,
    login_required
    )
from sqlalchemy import select

from . import app, db
from .models import *
from .forms import Regist_Form, Login_Form

@app.before_request
def before():
    if current_user.is_authenticated:
        g.scored = Song.query.join(Score,
            (Score.song_id==Song.id)).\
            filter(Score.user_id==current_user.id).\
            order_by(Song.title).all()
    else:
        g.scored = None


@app.route('/')
@app.route('/index')
def index():
    import random
    news = Song.query.all()
    random.shuffle(news)
    slide = news[0:7]
    return render_template('index.html', slide=slide)


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


@app.route('/artist/')
def artists():
    artists = Artist.query.order_by(Artist.name)
    return render_template('artists.html', artists=artists)


@app.route('/songs/')
def songs():
    song_list = Song.query.all()
    artist_list = Artist.query.all()
    return render_template('songs.html', song_list=song_list,
        artist_list=artist_list)


@app.route('/songs/<id>')
def song(id):
    act_song = Song.query.filter_by(id=id).first()
    year = int(act_song.year)
    if current_user.is_authenticated:
        id_user = current_user.id
        check = Score.query.filter(Score.user_id==id_user,
        Score.song_id==id).first()
        if check:
            score = check.score
        else:
            score = 100
    else:
        score = 0
    return render_template('song.html', title=act_song.title, act_song=act_song,
        year=year, score=score)


@app.route('/set_score', methods=['GET', 'POST'])
def set_score():
    score = request.form['score']
    song_id = request.form['song_id']
    check = Score.query.filter(Score.user_id==current_user.id,
    Score.song_id==(song_id)).first()
    id = current_user.id
    if check:
        check.score = score
        db.session.add(check)
        db.session.commit()
    else:
        add = Score(user_id=id, song_id=int(song_id),
        score=int(score), date=datetime.datetime.utcnow())
        db.session.add(add)
        db.session.commit()

    return jsonify({ "result": "OK" })