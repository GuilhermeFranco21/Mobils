# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from apps.home import blueprint
from flask import render_template, request, redirect, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import PaymentMethods, Debts, DebtInstallment
from datetime import datetime
from dateutil.relativedelta import relativedelta


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index2.html', segment='index')

#--------------------------------------------------------------------------------//---------------------------------------------------------------------------
@blueprint.route('/registerPayMethod', methods=["POST",])
@login_required
def registerPayment():
    print("Forma de pagamento registrada")
    
    description = request.form["inputDescription"]
    
    payment_method = PaymentMethods(description=description)
    db.session.add(payment_method)
    db.session.commit()
    
    print("Descrição: ", payment_method)

    return redirect('/listaFormaPagamento')


@blueprint.route('/listaFormaPagamento')
@login_required
def listPayment():
    list = PaymentMethods.query.order_by(PaymentMethods.id)
    print(list)
    return render_template('home/lista-forma-pagamento.html', list=list)


@blueprint.route('/editarFormaPagamento/<int:id>')
@login_required
def editPayment(id):
    
    payment_method = PaymentMethods.query.filter_by(id=id).first()

    return render_template("home/edita-forma-pagamento.html", payment=payment_method)


@blueprint.route('/updatePayMethod', methods=["POST"])
@login_required
def updatePayment():
    payment_method = PaymentMethods.query.filter_by(id=request.form["id"]).first()
    payment_method.description = request.form["inputDescription"]
    
    db.session.add(payment_method)
    db.session.commit()
    
    return redirect("/listaFormaPagamento")


@blueprint.route('/deletarFormaPagamento/<int:id>')
@login_required
def deletePayment(id):
    
    payment_method = PaymentMethods.query.filter_by(id=id).delete()
    
    db.session.commit()
    
    return redirect("/listaFormaPagamento")
    
#--------------------------------------------------------------------------------//---------------------------------------------------------------------------
#Rotas das dividas

@blueprint.route('/cadastrarDivida')
@login_required
def createDebt():
    print("Cadastrando divida")
    list_payment_methods = PaymentMethods.query.order_by(PaymentMethods.id)
    return render_template("home/cadastro-divida.html", list_payment=list_payment_methods)

@blueprint.route('/registerDebt', methods=["POST",])
@login_required
def registerDebt():
    print("Divida registrada com sucesso")
    count = 1
    
    creditor = request.form["inputCreditorName"]
    amount = request.form["inputValue"]
    description = request.form["inputDescription"]
    payment_method = request.form["inputFormPayment"]
    number_installments = request.form["inputInstallmentQuantity"]
    payment_date = request.form["inputDate"]
    
    payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
    
    id_payment_methods = PaymentMethods.query.filter_by(description=payment_method).first().id
    installment_value = float(amount)/int(number_installments)
    
    final_date = payment_date + relativedelta(months=int(number_installments)-1)
    
    print("type: ", id_payment_methods)
    print([creditor, amount, description, payment_method, number_installments, payment_date, final_date, installment_value])
    
    
    debt = Debts(creditor=creditor, amount=amount, description=description, id_payment_methods=id_payment_methods, number_installments=number_installments, installment_value=installment_value, initial_date=payment_date, final_date=final_date, pay=False)
    
    db.session.add(debt)
    db.session.commit()
    
    while count <= int(number_installments):
        payment_date = payment_date + relativedelta(months=1)
        debt_Installment = DebtInstallment(id_debt=debt.id, installment_value=installment_value, payment_date=payment_date, installment_number=count, payed="N")
        
        db.session.add(debt_Installment)
        db.session.commit()
        
        count = count + 1
    return redirect('/listaDividas')

@blueprint.route('/listaDividas')
@login_required
def listDebt():
    list = Debts.query.order_by(Debts.id)
    return render_template('home/lista-dividas.html', list=list)

@blueprint.route('/deletarDivida/<int:id>')
@login_required
def deleteDebt(id):
    
    debt = Debts.query.filter_by(id=id).delete()
    debt_installment = DebtInstallment.query.filter_by(id_debt=id).delete()
    db.session.commit()
    
    return redirect("/listaDividas")


@blueprint.route('/resumoDivida/<int:id>')
@login_required
def summaryDebt(id):
    debt = Debts.query.filter_by(id=id).first()
    payment_method_id = debt.id_payment_methods
    payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
    debt_installement = DebtInstallment.query.filter_by(id_debt=id)

    return render_template("home/resumo-divida.html", debt=debt, payment=payment_method, installment=debt_installement)


@blueprint.route('/editarDivida/<int:id>')
@login_required
def editDebt(id):
    debt = Debts.query.filter_by(id=id).first()
    list_payment_methods = PaymentMethods.query.order_by(PaymentMethods.id)
    
    return render_template("home/editar-divida.html", debt=debt, list_payment=list_payment_methods)

@blueprint.route('/updateDebt', methods=["POST"])
@login_required
def updateDebt():
    
    print("Entrei no update")
    
    count = 1
    
    creditor = request.form["inputCreditorName"]
    amount = request.form["inputValue"]
    description = request.form["inputDescription"]
    payment_method = request.form["inputFormPayment"]
    number_installments = request.form["inputInstallmentQuantity"]
    payment_date = request.form["inputDate"]
    
    payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
    
    id_payment_methods = PaymentMethods.query.filter_by(description=payment_method).first().id
    installment_value = float(amount)/int(number_installments)
    
    final_date = payment_date + relativedelta(months=int(number_installments)-1)
    
    debt = Debts.query.filter_by(id=request.form["id"]).first()
    debt.creditor = creditor
    debt.amount = amount
    debt.description = description
    debt.id_payment_methods = id_payment_methods
    debt.installment_value = installment_value
    debt.initial_date = payment_date
    debt.final_date = final_date
    debt.number_installments = number_installments
    
    db.session.add(debt)
    db.session.commit()
    
    number_installments = int(number_installments)
    
    debt_installment = DebtInstallment.query.filter_by(id_debt=request.form["id"]).all()
    
    
    
    for installment in debt_installment:
       
        if installment.installment_number > number_installments:
            debt_installment = DebtInstallment.query.filter_by(id=installment.id).delete()
            db.session.commit()
        
        else:
            if count == 1:
                installment.payment_date = payment_date
                
            
            else:
                payment_date = payment_date + relativedelta(months=1)
                installment.payment_date = payment_date
            
            installment.installment_number = count
            installment.installment_value = installment_value

            db.session.add(installment)
            db.session.commit()
            count += 1
    
    print(count)
    while count - 1 < int(number_installments):
        payment_date = payment_date + relativedelta(months=1)
        
        debt_Installment = DebtInstallment(id_debt=debt.id, installment_value=installment_value, payment_date=payment_date, installment_number=count, payed="N")
        db.session.add(debt_Installment)
        db.session.commit()
        count += 1
    
    return redirect("/listaDividas")

@blueprint.route('/parcelaDivida/<int:id>', methods=["GET",])
@login_required
def installmentDebt(id):
    debt_installment = DebtInstallment.query.filter_by(id=id).first()
    

    if debt_installment.payed == "N":
        debt_installment.payed = "S"
    
    else:    
        debt_installment.payed = "N"
    
    db.session.add(debt_installment)
    db.session.commit()

    return redirect("/resumoDivida/" + str(debt_installment.id_debt))

#--------------------------------------------------------------------------------//---------------------------------------------------------------------------
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
