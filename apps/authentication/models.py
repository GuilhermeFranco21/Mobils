# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager 

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    

#Login
@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
#Fim login

class PaymentMethods(db.Model):

    __tablename__ = 'Payment_Methods'
    
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id))
    description = db.Column(db.String(150))
    
    def __repr__(self):
        return str(self.description, self.id)


class Debts(db.Model):
    
    __tablename__ = 'Debts'
    
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id))
    creditor = db.Column(db.String(150))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(150))
    id_payment_methods = db.Column(db.Integer, db.ForeignKey(PaymentMethods.id))
    number_installments = db.Column(db.String(60))
    installment_value = db.Column(db.Float)
    initial_date = db.Column(db.Date)
    final_date = db.Column(db.Date)
    pay = db.Column(db.Boolean)
    
    
    def __repr__(self):
        return str(self.description)

class DebtInstallment(db.Model):
    
    __tablename__ = 'Debt_Installment'
    
    id = db.Column(db.Integer, primary_key=True)
    id_debt = db.Column(db.Integer, db.ForeignKey(Debts.id))
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id)) #Para filtrar por user
    installment_value = db.Column(db.Float)
    payment_date = db.Column(db.Date)
    installment_number = db.Column(db.Integer)
    payed = db.Column(db.String(1))

    def __repr__(self):
        return str(self.id)


class PerfilUser(db.Model):
    
    __tablename__ = 'Perfil_User'
    
    id = db.Column(db.Integer, primary_key=True) 
    id_user = db.Column(db.Integer, db.ForeignKey(Users.id))
    nome = db.Column(db.String(60))
    sobrenome = db.Column(db.String(60))
    numero_telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(100))
    cep = db.Column(db.String(10))
    #email vai pegar do objeto user
    cidade = db.Column(db.String(60))
    uf = db.Column(db.String(60))
    imgPerfil = db.Column(db.String(100))#imagem para o perfil
    
    
# Pagina index - mostrar valores, valor total de dividas, quantidade de dividas, 
# Valor total pago, contas nao paga

