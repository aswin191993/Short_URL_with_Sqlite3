from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,TextField,PasswordField,IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = TextField('openid', validators=[DataRequired()])

class SigninForm(Form):
    idu = StringField('idu', validators=[DataRequired()])
    
