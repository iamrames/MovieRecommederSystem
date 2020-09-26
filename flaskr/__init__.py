import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mrs.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Adding a CLI command for initializing Database
    ## Use Command `flask init-db` to initialize db
    from . import db
    db.init_app(app)

    ## Use Command `flask insert-users` to create users
    db.create_users(app)

    ## Use Command `flask insert-movies` to create movies
    db.create_movies(app)

    ## Use Command `flask insert-ratings` to create ratings
    db.create_ratings(app)

    ## Use Command `flask insert-genre` to create movie genre
    db.create_genres(app)

    ## Importing and registering the blueprint from the factory using app.register_blueprint().
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import itemBasedCF
    app.register_blueprint(itemBasedCF.bp)

    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app