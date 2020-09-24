import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import pandas as pd, numpy as np
import random, string
from werkzeug.security import  generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('insert-users')
@with_appcontext
def create_user():
    db = get_db()
    chunksize = 100
    r_cols = ['id', 'age' , 'gender' , 'occupation' , 'zip_code']
    path = 'D:\Videos\Tutorials\MACHINE LEARNING\[FreeTutorials.Us] Udemy -  data-science-and-machine-learning-with-python-hands-on\DataScience-Python3\ml-100k/u.user'
    # users = pd.read_csv(path,  sep='|',names=r_cols, usecols=range(5), encoding="ISO-8859-1")
    for chunk in pd.read_csv(path,  sep='|',names=r_cols, usecols=range(5), encoding="ISO-8859-1", chunksize=chunksize):
        chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
        username = get_random_usernames(len(chunk))
        password = get_random_password(len(chunk))
        dict = {'username': username, 'password': password,'id': chunk['id']}  
        df = pd.DataFrame(dict) 
        finalData = pd.merge(chunk, df)
        finalData.to_sql(name='user', con=db, if_exists='append', index=False)
    click.echo('All User created.')

def create_users(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_user)

@click.command('insert-movies')
@with_appcontext
def create_movie():
    db = get_db()
    chunksize = 50
    r_cols = ['id' , 'title' , 'release_date' , 'video_release_date' ,
              'IMDB_URL' , 'unknown' , 'Action' , 'Adventure' , 'Animation' ,
              'Childrens' , 'Comedy' , 'Crime' , 'Documentary' , 'Drama' , 'Fantasy' ,
              'Film-Noir' , 'Horror' , 'Musical' , 'Mystery' , 'Romance' , 'Sci-Fi' ,
              'Thriller' , 'War' , 'Western']
    path = 'D:\Videos\Tutorials\MACHINE LEARNING\[FreeTutorials.Us] Udemy -  data-science-and-machine-learning-with-python-hands-on\DataScience-Python3\ml-100k/u.item'
    for chunk in pd.read_csv(path,  sep='|',names=r_cols, usecols=range(23), encoding="ISO-8859-1", chunksize=chunksize):
        chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
        chunk.to_sql(name='movies', con=db, if_exists='append', index=False)
    click.echo('All Movies created.')

def create_movies(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_movie)


@click.command('insert-ratings')
@with_appcontext
def create_rating():
    db = get_db()
    chunksize = 100
    r_cols = ['user_id', 'item_id' , 'rating' , 'timestamp']
    path = 'D:\Videos\Tutorials\MACHINE LEARNING\[FreeTutorials.Us] Udemy -  data-science-and-machine-learning-with-python-hands-on\DataScience-Python3\ml-100k/u.data'
    for chunk in pd.read_csv(path,  sep='\t',names=r_cols, usecols=range(4), encoding="ISO-8859-1", chunksize=chunksize):
        chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
        chunk.to_sql(name='user_ratings', con=db, if_exists='append', index=False)
    click.echo('All user ratings created.')

def create_ratings(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(create_rating)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = 'user_'.join(random.choice(letters) for i in range(length))
    return result_str

def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    # Convert string to list and shuffle it to mix letters and digits
    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string

def get_random_usernames(count):
    username = []
    for i in range(count):
	    username.append(get_random_string(6))
    return username

def get_random_password(count):
    password = []
    for i in range(count):
	    password.append(generate_password_hash('password'))
    return password
