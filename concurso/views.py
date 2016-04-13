import datetime

from flask import (render_template, redirect, url_for,
    flash, request, jsonify, g)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required, session)
from flask.ext.babel import gettext as _

from . import app, db, babel
from .models import *
from .forms import LoginForm
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = form._user

        login_user(user)

        session['font'] = '18px'    # XXX: Check for alternative

        flash(_('Welcome <b>%(email)s</b>!', email=user.email), 'success')

        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['font'] = '18px'
    logout_user()
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
    if session['font'] == '18px':
        session['font'] = '24px'
    else:
        session['font'] = '18px'
    return redirect(next)
