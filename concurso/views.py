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
    return request.accept_languages.best_match(LANGUAGES.keys())


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
            return redirect(url_for('login'))
        else:
            login_user(u)
            session['font'] = '18px'
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """
    Logs the user out and restores the font size
    """
    session['font'] = '18px'
    logout_user()
    return redirect(url_for('index'))


@app.route('/songs/')
def songs():
    """
    List out all the songs and artists in the database
    """
    song_list = Song.query.all()
    artist_list = Artist.query.all()
    return render_template('songs.html', song_list=song_list,
        artist_list=artist_list)


@app.route('/songs/<id>')
def song(id):
    """
    Retrieves an specific song and checks if the current_user
    has rated it or not.
    """
    artist_list = Artist.query.all()
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
        score=score, video=video,
        artist_list=artist_list)


@app.route('/set_score', methods=['GET', 'POST'])
def set_score():
    """
    Inserts applies a score from a user to a song 
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
    return jsonify({ "result": "OK" })

    

@app.route('/set_font', methods=['GET', 'POST'])
def set_font():
    """
    Changes the font of the entire website.
    """
    if session['font'] == '18px':
        session['font'] = '24px'
    else:
        session['font'] = '18px'
    return jsonify({ "result": "OK" })