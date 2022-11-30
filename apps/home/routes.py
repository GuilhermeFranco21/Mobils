# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from apps.home import blueprint
from flask import render_template, request, redirect, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import PaymentMethods


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

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
