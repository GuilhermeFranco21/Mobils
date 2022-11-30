from flask_wtf import FlaskForm
from wtforms import StringField

class RegisterPayMethodForm(FlaskForm):
    description = StringField('Descrição', id='description_register',)