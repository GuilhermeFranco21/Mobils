from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField

class RegisterPayMethodForm(FlaskForm):
    description = StringField('Descrição', id='description_register',)
    

class RegisterDebtsForm(FlaskForm):
    creditor = StringField('Credor', id='creditor_register',)
    debt_value = FloatField('Valor da Divida', id='debt_value_register',)
    description = StringField('Descrição', id='description_register',)
    payment_method = StringField('Forma de Pagamento', id='payment_method_register',)
    number_installments = StringField('Numero de Parcelas', id='number_installments_register',)
    payment_date = DateField('Descrição', id='description_register',)