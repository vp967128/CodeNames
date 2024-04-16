from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from flask_bcrypt  import Bcrypt
from flask_cors import CORS
import events
import uuid
from classes import *

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config["SECRET_KEY"] = 'mysecret'
app.config['DEBUG'] = True
app.register_blueprint(events.game)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'

bcrypt = Bcrypt(app) 
db.init_app(app)
admin.init_app(app)
events.socketio.init_app(app)



@app.errorhandler(404)
def page_not_found(e):
    flash("Page Not Found")
    return redirect(url_for("login"))

@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authenticated. Please login")
    return redirect(url_for("login"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User(name=request.form.get("name"),
                    email=request.form.get("email"),
                    password=bcrypt.generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()
        
        if request.form.get("remember") == "on":
            login_user(user, remember=True)
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/forgot_password')
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if 'user_id' not in session:
        # Generate a new user ID for the first-time user
        session['user_id'] = str(uuid.uuid4())
    if current_user.is_authenticated:
        return redirect(url_for("lounge"))
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form.get("email")).first()
        # pw_hash = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')


        if user and bcrypt.check_password_hash(user.password, request.form.get("password")):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for('lounge'))
        else:
            flash("Invalid username or password")
            print("INVALID!!!!!!!!!!!!!!")
    return render_template("login.html")


@app.route("/lounge")
@login_required
def lounge():
    return render_template("lounge.html")

if __name__ == "__main__":
   app.run(debug=True)