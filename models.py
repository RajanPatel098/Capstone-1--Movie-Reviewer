from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

brcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)


class User(db.Model):
    """USERS INFO"""
    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """REGISTERING A USER AND HASHING PASS"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """VALIDATE USER AND PASS EXIST AND CORRECT"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Ratings(db.Model):
    """MOVIES RATINGS"""
    __tablename__ = "ratings"
    
    id = db.Column(db.Integer, primary_key=True)
