from flask import Flask, redirect, render_template, jsonify, session, g, flash, request
from models import db, connect_db, User, Ratings
from forms import LoginForm, RegisterForm
from sqlalchemy.exc import IntegrityError
import requests
from bs4 import BeautifulSoup

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "rpatMovies"
### omdbapi.com/?t=[title]&y=[year]&apikey=78ff9c4d

API_KEY= "78ff9c4d"
# movie = GetMovie(api_key='78ff9c4d')  -> gives all info using omdbapi 

@app.route('/',methods=["POST","GET"])
def home():
    if request.method == "POST":
        title = request.args.get('title')
        response = requests.get('https://www.omdbapi.com/?t={title}&apikey={API_KEY}')
        response.raise_for_status()
        print(response)

        json_data = json.loads(response.text)

        print(json_data['year'], json_data['Rated'], json_data['Released'])
        return render_template("base.html",info=MovieInfo)

    return render_template("base.html")

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("YOU JAVE LOGGED OUT.", 'success')
    return redirect("/login")
