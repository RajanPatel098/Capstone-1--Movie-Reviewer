import os 
import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, jsonify, session, g, flash, request
from models import db, connect_db, User, Rating
from forms import LoginForm, RegisterForm, RatingForm
from sqlalchemy.exc import IntegrityError
from secrets import API_SECRET_KEY, DB_SECRET_KEY


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///capstone'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', DB_SECRET_KEY)
### omdbapi.com/?t=[title]&y=[year]&apikey=xxxxxx

API_KEY= API_SECRET_KEY
# movie = GetMovie(api_key)  -> gives all info using omdbapi 

@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        title = {details.title}
        db.session.add(title)

    return render_template("base.html")

### User Sign up/login/ logout

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

### GENERAL USER ROUTES

@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging ratings in order from the database;
    # user.ratings won't be in order by default
    ratings = (Rating
                .query
                .filter(Rating.user_id == user_id)
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, ratings=ratings)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


## RATINGS ROUTES
@app.route('/ratings/new', methods=["GET", "POST"])
def ratings_add():
    """Add a rating:

    Show form if GET. If valid, update rating and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = RatingForm()

    if form.validate_on_submit():
        rtg = Rating(text=form.text.data)
        g.user.ratings.append(rtg)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('ratings/new.html', form=form)


@app.route('/ratings/<int:rating_id>', methods=["GET"])
def ratings_show(rating_id):
    """Show a rating."""

    rtg = Rating.query.get(rating_id)
    return render_template('ratings/show.html', rating= rtg)


@app.route('/ratings/<int:rating_id>/delete', methods=["POST"])
def ratings_destroy(rating_id):
    """Delete a rating."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    rtg = Rating.query.get(rating_id)
    db.session.delete(rtg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")





