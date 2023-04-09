from flask import Flask, redirect, render_template, jsonify, session, g, flash, request
from models import db, connect_db, User, Rating
from forms import LoginForm, RegisterForm, Rating
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
def index():
    if request.method == "POST":
        title = {details.title}
        db.session.add(title)

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

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    ratings = (Rating
                .query
                .filter(ratings.user_id == user_id)
                .order_by(ratings.timestamp.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, ratings=ratings)

## RATINGS ROUTES
@app.route('/ratings/new', methods=["GET", "POST"])
def ratings_add():
    """Add a rating:

    Show form if GET. If valid, update rating and redirect to user page.
    """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = Rating()

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



@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("YOU JAVE LOGGED OUT.", 'success')
    return redirect("/login")
