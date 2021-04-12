import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import click
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import time

bp = Blueprint('movies', __name__)

@bp.route('/movies')
@login_required
def index():
    user_id = g.user
    if user_id is None:
        user_id = 0
    else:
        user_id = user_id['id']
    movies = correlate_all_movies(user_id)
    return render_template('movies/index.html', movies=movies)

@bp.route('/movies/search', methods=('GET', 'POST'))
def search():
    keyword = request.form['keyword']
    db = get_db()
    # movies = db.execute(
    #     'SELECT id, Title, IMDB_URL, Image_URL, musical, mystery, romance, [Sci-Fi], thriller, war, western, unknown, action, adventure, animation, childrens, comedy, crime, documentary, drama, fantasy, [film-noir], horror FROM movies WHERE Title like ?',
    #     ("%"+keyword+"%",)
    # ).fetchall()
    movies = db.execute("""
        SELECT title, ifnull(rating/count,0) rating, movies.id, movies.IMDB_URL, movies.Image_URL, movies.movie_desc  from movies 
        left join (SELECT item_id, SUM(rating) rating, count(rating) count from user_ratings group by item_id) ratings on ratings.item_id = movies.id
        WHERE Title like ?
    """,("%"+keyword+"%",)).fetchmany(66)
    data = []
    for row in movies:
        data.append([x for x in row]) # or simply data.append(list(row))
    return render_template('movies/movielists.html', movies_info=movies)

@bp.route('/movies/list')
def list():
    db = get_db()

    avg_rating = db.execute("""
    SELECT title, ifnull(rating/count,0) rating, movies.id, movies.IMDB_URL, movies.Image_URL, movies.movie_desc  from movies 
    left join (SELECT item_id, SUM(rating) rating, count(rating) count from user_ratings group by item_id) ratings on ratings.item_id = movies.id
    """).fetchmany(66)

    return render_template('movies/movielists.html', movies_info=avg_rating)

@bp.route('/movies/myratings')
def myratings():
    user_id = g.user
    if user_id is None:
        user_id = 0
    else:
        user_id = user_id['id']

    db = get_db()
    avg_rating = db.execute("""
    SELECT title, ifnull(rating/count,0) rating, movies.id, movies.IMDB_URL, movies.Image_URL, movies.movie_desc  from movies 
    inner join (SELECT user_id, item_id, SUM(rating) rating, count(rating) count from user_ratings where user_id = ?
	group by item_id, user_id) ratings on ratings.item_id = movies.id
    """,(user_id,)).fetchmany(66)

    return render_template('movies/movielists.html', movies_info=avg_rating)

@bp.route('/movies/category/<category>')
def get_movie(category):
    db = get_db()
    arg = f'{category} = 1'
    # query = 'SELECT id, Title, IMDB_URL, Image_URL FROM movies WHERE [{}]'.format(category)
    query = """
        SELECT title, ifnull(rating/count,0) rating, movies.id, movies.IMDB_URL, movies.Image_URL, movies.movie_desc  from movies 
        left join (SELECT item_id, SUM(rating) rating, count(rating) count from user_ratings group by item_id) ratings on ratings.item_id = movies.id
        WHERE [{}]
    """.format(category)
    movies = db.execute(query).fetchmany(66)
    return render_template('movies/movielists.html', movies_info=movies)

def correlate_all_movies(user_id):
    db = get_db()
    ratings = db.execute(
        'SELECT user_id,item_id as movie_id,rating FROM user_ratings'
    ).fetchall()
    movies = db.execute(
        'SELECT id as movie_id,title FROM movies'
    ).fetchall()
    ratings_df = pd.DataFrame(ratings, columns= ['user_id','movie_id','rating'])
    movies_df = pd.DataFrame(movies, columns= ['movie_id','title'])
    ratings = pd.merge(movies_df, ratings_df)

    userRatings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')
    corrMatrix = userRatings.corr(method='pearson', min_periods=100)
    # getting correlated rating by user id
    if(user_id in userRatings.index):
        myRatings = userRatings.loc[user_id].dropna()
    else:
        myRatings = userRatings.dropna()
    
    simCandidates = pd.Series()
    for i in range(0, len(myRatings.index)):
        # "Adding sims for myRatings.index[i]
        # Retrieve similar movies to this one that I rated
        sims = corrMatrix[myRatings.index[i]].dropna()
        # Now scale its similarity by how well I rated this movie
        sims = sims.map(lambda x: x * myRatings[i])
        # Add the score to the list of similarity candidates
        simCandidates = simCandidates.append(sims)
    
    #Glance at our results so far:
    # "sorting..."
    simCandidates.sort_values(inplace = True, ascending = False)

    simCandidates = simCandidates.groupby(simCandidates.index).sum()

    simCandidates.sort_values(inplace = True, ascending = False)

    filteredSims = simCandidates.drop(myRatings.index,errors = 'ignore')
    movies_list = filteredSims.index.tolist()
    query= f"SELECT title, IMDB_URL, Image_URL, movie_desc FROM movies where title in ({','.join(['?']*len(movies_list))})"
    topmovies = db.execute(query, movies_list).fetchmany(66)
    return topmovies

@bp.route('/movies/<movie_id>/<rating>/ratemovie', methods=('GET', 'POST'))
@login_required
def ratemovie(movie_id,rating):
    user_id = g.user
    if user_id is None:
        user_id = 0
    else:
        user_id = user_id['id']
    
        item_id = movie_id
        rating = rating
        error = None

    if not movie_id:
        error = 'Select valid movie..'

    if not rating:
        error = 'Rating is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO user_ratings (user_id, item_id, rating, timestamp)'
            ' VALUES (?, ?, ?, ?)',
            (user_id, item_id, rating, time.time())
        )
        db.commit()
        return redirect(url_for('movies.list'))

    return redirect(url_for('movies.list'))