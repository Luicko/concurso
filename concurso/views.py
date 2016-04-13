import datetime

from flask import render_template, redirect, url_for, flash, request, jsonify, g
from flask.ext.login import (login_user, logout_user, current_user,
    login_required, session
    )

from . import app, db, babel
from .models import *
from .forms import Regist_Form, Login_Form
from settings import LANGUAGES


@babel.localeselector
def get_locale():
    return 'es' #request.accept_languages.best_match(LANGUAGES.keys())


@app.before_request
def before():
    """
    Creates a list from all the songs that the current_user has rated.
    """
    from string import ascii_uppercase
    g.alphabet = ascii_uppercase
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
    query = Song.query.all()
    random.shuffle(query)
    slide = query[0:7]
    return render_template('index.html', slide=slide)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login_Form()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if not u:
            flash('Couldn\'t log in')
            return redirect(url_for('login'))
        else:
            login_user(u)
            session['font'] = '18px'
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['font'] = '18px'
    logout_user()
    return redirect(url_for('index'))


@app.route('/songs/')
def songs():
    song_list = Song.query.all()
    artist_list = Artist.query.all()
    return render_template('songs.html', song_list=song_list,
        artist_list=artist_list)


@app.route('/songs/<id>')
def song(id):
    """
    Retrieves the an specific song and checks if the current_user
    has rated.
    """
    song = Song.query.filter_by(id=id).first_or_404()
    year = int(song.year)
    with app.open_resource('static/video/'+str(id)+'.link') as file:
        video = file.read()
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
    return render_template('song.html', title=song.title,
        song=song, year=year,
        score=score, video=video)


@app.route('/set_score', methods=['GET', 'POST'])
def set_score():
    """
    Inserts a new Score from a user to a song 
    or updates an existing one.
    """
    score = request.form.get('score', 0, type=int)
    song_id = request.form['song_id']
    check = Score.query.filter(Score.user_id==current_user.id,
    Score.song_id==(song_id)).first()
    id_user = current_user.id
    if check:
        check.score = score
        db.session.add(check)
        db.session.commit()
    else:
        query = Score.query.order_by(Score.id.desc()).first()
        last = int(query.id) + 1
        add = Score(id=last, user_id=id_user, song_id=int(song_id),
        score=int(score), date=datetime.datetime.utcnow())
        db.session.add(add)
        db.session.commit()

    

@app.route('/set_font', methods=['GET', 'POST'])
def set_font():
    """
    Inserts a new Score from a user to a song 
    or updates an existing one.
    """
    if session['font'] == '18px':
        session['font'] = '24px'
    else:
        session['font'] = '18px'
    return jsonify({ "result": "OK" })