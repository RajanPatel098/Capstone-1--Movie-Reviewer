from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """USERS INFO"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)


    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Movie(db.Model):
    """MOVIE FROM API"""
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    genre = db.Column(db.Text, nullable=False)

class Ratings(db.Model):
    """MOVIES RATINGS"""
    __tablename__ = "ratings"
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    

class userList(db.Model):
    """USERS FAVORITE MOVIES LIST"""
    __tablename__ = "userslists"

    id = db.Column(db.Integer, primary_key=True)
    listTitle = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    

def connect_db(app):
    """Connect this database to provided Flask app.

    """

    db.app = app
    db.init_app(app)