import datetime

from flask import (render_template, redirect, url_for,
    flash, request, jsonify, g)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required, session)
from flask.ext.babel import gettext as _
from werkzeug.security import generate_password_hash, \
     check_password_hash
from sqlalchemy import func

from . import app, db, babel
from .models import *
from .forms import LoginForm, RegistrationForm
from .utils import get_redirect_target


@app.before_request
def before():
    """
    Creates a list from all the songs that the current_user has rated.
    """
    from string import ascii_uppercase
    g.alphabet = ascii_uppercase

    g.scored = []

    if current_user.is_authenticated:
        g.scored = Song.query.join(Score,
            (Score.song_id==Song.id)) \
            .filter(Score.user_id==current_user.id) \
            .order_by(Song.title).all()


@app.route('/')
@app.route('/index')
def index():
    import random
    songs = Song.query.all()
    random.shuffle(songs)
    slide = songs[0:7]

    return render_template('index.html', slide=slide)

@app.route('/sign in', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if not u:
            flash('Error al iniciar sesion')
            return redirect(url_for('login'))
        elif check_password_hash(u.password, form.password.data):
            session['font'] = '17px'    # XXX: Check for alternative
            login_user(u)
            return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')



@app.route('/signup', methods=['GET', 'POST'])
def regist():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(email=form.email.data, name=form.nickname.data, 
            password=generate_password_hash(form.password.data), birthday=form.birthday.data, signindate=datetime.datetime.utcnow())
        db.session.add(u)
        db.session.commit()
        flash('Thank you for joinin!!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, title='Sign Up')


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/songs/')
def songs():
    songs = Song.query
    artists = Artist.query
    return render_template('songs.html', songs=songs, artists=artists)


@app.route('/songs/<id>')
def song(id):
    """
    Retrieves an specific song and checks if the current_user
    has rated it or not.
    """
    song = Song.query.filter_by(id=id).first_or_404()

    score = 0

    with app.open_resource('static/video/{}.link'.format(id)) as f:
        video = f.read()

    if current_user.is_authenticated:
        score = Score.query.filter(
            Score.user_id==current_user.id,
            Score.song_id==id).first()
        if score:
            score = score.score
        else:
            score = 100

    return render_template('song.html', song=song, score=score,
            video=video)


@app.route('/set_score', methods=['GET', 'POST'])
def set_score():
    """
    Inserts applies a score from a user to a song 
    or updates an existing one.
    """
    val = request.form.get('score', 0, type=int)
    song_id = request.form.get('song_id', type=int)

    song = Song.query.filter_by(id=song_id).first_or_404()

    score = Score.query.filter(
            Score.user_id==current_user.id,
            Score.song_id==song_id).first()
    if score:
        score.score = val
        db.session.add(score)
        db.session.commit()
    else:
        score = Score(user_id=current_user.id, song_id=song_id,
                      score=val, date=datetime.datetime.utcnow())
        db.session.add(score)
        db.session.commit()

    return jsonify({ "result": "OK" })


@app.route('/set_font', methods=['GET', 'POST'])
def set_font():
    """
    Changes the font of the entire website.
    """
    next = get_redirect_target()
    if session['font'] == '17px':
        session['font'] = '22px'
    else:
        session['font'] = '17px'
    return redirect(next)


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/most rated')
def most_rated():
    bars = []
    songs = []
    group = x = db.session.query(func.sum(Score.score),\
        Score.song_id).group_by(Score.song_id).\
        order_by(func.sum(Score.score).desc()).limit(5)
    top = group[0]
    for song in group[1:4]:
        width = str(((int(song[0])*80)/int(top[0])))+'%'
        bars.append((width, song[1]))
    for song in group:
        new = Song.query.filter(Song.id==song[1]).first()
        songs.append(new)
    return render_template('top.html', top=top, group=group, bars=bars, songs=songs) 