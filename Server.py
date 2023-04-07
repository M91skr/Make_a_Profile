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
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length


# ----------------------------------------  class to use Flask-wtf Creation ----------------------------------------


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[Email()])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')


app = Flask(__name__)
app.secret_key = "SECRET_KEY"
Bootstrap(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    login_data = LoginForm()
    login_data.validate_on_submit()
    if login_data.validate_on_submit():
        if login_data.email.data == "admin@email.com" and login_data.password.data == "12345678":
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_data)


if __name__ == '__main__':
    app.run(debug=True)
