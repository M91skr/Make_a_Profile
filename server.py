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
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# ----------------------------------------  Flask App Creation ----------------------------------------


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=request.form.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("success"))
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory(directory='static', path="files/cheat_sheet.pdf")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     login_data = LoginForm()
#     login_data.validate_on_submit()
#     if login_data.validate_on_submit():
#         if login_data.email.data == "admin@email.com" and login_data.password.data == "12345678":
#             return render_template('success.html')
#         else:
#             return render_template('denied.html')
#     return render_template('login.html', form=login_data)


if __name__ == '__main__':
    app.run(debug=True)
