"""---------------------------------------- Make a Profile ----------------------------------------
In this site, we use Flask to create a site where the user can log in and see their security information.
To create the following site, I took help from the following documents:
Using wtf 😂: https://wtforms.readthedocs.io/en/2.3.x/forms/;
Definition of functional fields: https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectField;
Validation of fields: https://wtforms.readthedocs.io/en/2.3.x/validators/#module-wtforms.validators;
Error handling: https://wtforms.readthedocs.io/en/2.3.x/crash_course/#displaying-errors;
(Create more attractive UX: https://pythonhosted.org/Flask-Bootstrap/basic-usage.html)
"""

# ---------------------------------------- Add Required Library ----------------------------------------
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# ----------------------------------------  Flask App Creation ----------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------------------------------- User Authenticate Management ----------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------------------------------  Database Creation ----------------------------------------


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("success"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('success'))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/success')
@login_required
def success():
    print(current_user.name)
    return render_template("success.html", name=current_user.name, logged_in=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf")


if __name__ == '__main__':
    app.run(debug=True)
