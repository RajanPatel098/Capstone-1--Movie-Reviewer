from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, DataRequired
from flask_wtf import FlaskForm

class RatingForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class RegisterForm(FlaskForm):
    """REGISTRATION FORM."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

class UserList(FlaskForm):
    """FORM FOR MAKING MOVIE PLAYLISTS"""

    title = StringField(
        "Movie List Name",
        validators=[InputRequired()]
    )
    description = StringField(
        "Description",
        validators=[InputRequired()]
    )

class NewMovieForUserList(FlaskForm):
    """Form for adding a song to playlist."""

    movie = SelectField('Movie To Add', coerce=int)
