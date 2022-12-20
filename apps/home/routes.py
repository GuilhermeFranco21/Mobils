# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
import time
from apps import db
from datetime import datetime
from apps.home import blueprint
from apps.home.util import moeda
from jinja2 import TemplateNotFound
from dateutil.relativedelta import relativedelta
from flask_login import login_required, current_user
from flask import render_template, request, redirect, send_from_directory
from apps.authentication.models import PaymentMethods, Debts, DebtInstallment, PerfilUser
from apps.home.helpers import recupera_imagem, imgPerfil
from apps.home.Dividas.utils import CadastrarDividas, DeletarDividas
from apps.home.Dashboard.utils import DividaTotal, ContasNaoPagas, ContasPagas
from apps.home.MetodoPagamento.utils import registerPaymentMethod
from apps.home.Perfil.utils import EditarPerfil

@blueprint.route('/index')
@login_required
def index():
    # Filtra lista por user e limita quantidade
    list = Debts.query.filter_by(id_user=current_user.id).order_by(Debts.initial_date.desc()).limit(10)
    # Tratar quantidade de dividas, por id_user.
    qtdDividas = Debts.query.filter_by(id_user=current_user.id).count()
    # Calcula valor total da divida
    valorF = DividaTotal(id_user=current_user.id)
    # Contas nao pagas
    valorNaoPago = ContasNaoPagas(id_user=current_user.id)
    # Contas paga
    valorPago = ContasPagas(id_user=current_user.id)
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    
    return render_template('home/home-index.html', list=list, info=qtdDividas, valorDividaTotal=valorF, valorNaoPago=valorNaoPago, valorPago=valorPago, moeda=moeda, imagemUser=imagemUser)

# <----------------------- Rotas formas pagamento ----------------------->

# Rota de cadastro de forma de pagamento
@blueprint.route('/CadastrarFormaPagamento')
@login_required
def createPayment():
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    return render_template("home/forma-pagamento.html", imagemUser=imagemUser)


# Rota para registrar metooo de  pagamento
@blueprint.route('/registerPayMethod', methods=["POST",])
@login_required
def registerPayment():
    description = request.form["inputDescription"]
    # Funcao para registrar metodo de pagamento
    registerPaymentMethod(id_user=current_user.id, description=description)
    return redirect('/listaFormaPagamento')


# Rota para lista os metodos de pagamento
@blueprint.route('/listaFormaPagamento')
@login_required
def listPayment():
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    
    list = PaymentMethods.query.filter_by(id_user=current_user.id)
    return render_template('home/lista-forma-pagamento.html', list=list, imagemUser=imagemUser)


# Rotas de edicao Forma pagamento
@blueprint.route('/editarFormaPagamento/<int:id>')
@login_required
def editPayment(id):
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    payment_method = PaymentMethods.query.filter_by(id=id).first()
    return render_template("home/edita-forma-pagamento.html", payment=payment_method, imagemUser=imagemUser)


# Atualizar Metodo de pagamento
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

# <-------------------------- Rotas das dividas -------------------------->

#Rotas das dividas
@blueprint.route('/cadastrarDivida')
@login_required
def createDebt():
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    
    print("Cadastrando divida")
    
    list_payment_methods = PaymentMethods.query.filter_by(id_user=current_user.id)
    
    return render_template("home/cadastro-divida.html", list_payment=list_payment_methods, imagemUser=imagemUser)


# Cadastrar uma divida no DB
@blueprint.route('/registerDebt', methods=["POST",])
@login_required
def registerDebt():
    
    print("Divida registrada com sucesso")
    
    
    creditor = request.form["inputCreditorName"]
    amount = request.form["inputValue"]
    amount = float(amount)
    description = request.form["inputDescription"]
    payment_method = request.form["inputFormPayment"]
    number_installments = request.form["inputInstallmentQuantity"]
    payment_date = request.form["inputDate"]
    id_user=current_user.id
    
    #Funcão para cadastrar
    CadastrarDividas(creditor, amount, description, payment_method, number_installments, payment_date, id_user)
    
    return redirect('/listaDividas')


#Rota para acessar lista de dividas 
@blueprint.route('/listaDividas')
@login_required
def listDebt():
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    list = Debts.query.filter_by(id_user=current_user.id).order_by(Debts.id.desc())
    
    return render_template('home/lista-dividas.html', list=list, moeda=moeda, imagemUser=imagemUser)


#Rota para deletar divida
@blueprint.route('/deletarDivida/<int:id>')
@login_required
def deleteDebt(id):
    
    DeletarDividas(id=id)
    return redirect("/listaDividas")


#Resumo de dividas pelo id
@blueprint.route('/resumoDivida/<int:id>')
@login_required
def summaryDebt(id):
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    
    debt = Debts.query.filter_by(id=id).first()
    payment_method_id = debt.id_payment_methods
    payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
    debt_installement = DebtInstallment.query.filter_by(id_debt=id)
    
    return render_template("home/resumo-divida.html", debt=debt, payment=payment_method, installment=debt_installement, moeda=moeda, imagemUser=imagemUser) 

# Deletar dividas
@blueprint.route('/editarDivida/<int:id>')
@login_required
def editDebt(id):
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    
    debt = Debts.query.filter_by(id=id).first()
    list_payment_methods = PaymentMethods.query.order_by(PaymentMethods.id)
    return render_template("home/editar-divida.html", debt=debt, list_payment=list_payment_methods, imagemUser=imagemUser)


@blueprint.route('/updateDebt', methods=["POST"])
@login_required
def updateDebt():
    #deletar Divida - pelo request form
    debt = Debts.query.filter_by(id=request.form["id"]).delete()
    debt_installment = DebtInstallment.query.filter_by(id_debt=request.form["id"]).delete()
    db.session.commit()
    
    # Pegar no formulario do html
    creditor = request.form["inputCreditorName"]
    amount = request.form["inputValue"]
    description = request.form["inputDescription"]
    payment_method = request.form["inputFormPayment"]
    number_installments = request.form["inputInstallmentQuantity"]
    payment_date = request.form["inputDate"]
    id_user = current_user.id
    
    #Recriando dividas
    CadastrarDividas(creditor, amount, description, payment_method, number_installments, payment_date, id_user)
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

# <----------------------------- Rotas Perfil ----------------------------->

#Rota perfil
@blueprint.route('/perfil')
@login_required
def perfil():
    # Mostrar imagem do perfil do usuario
    imagemUser = imgPerfil(id_user=current_user.id)
    perfil = PerfilUser.query.filter_by(id_user=current_user.id).first()
    return render_template('home/tela-perfil.html', perfil=perfil, imagemUser=imagemUser)
#Editar Perfil
@blueprint.route('/editarPerfil', methods=["POST",])
@login_required
def editarPerfil():
    
    #Definir propriedades
    nome = request.form["nome"]
    sobrenome = request.form["sobrenome"]
    numero_telefone = request.form["numeroTelefone"]
    endereco = request.form["endereco"]
    cep = request.form["cep"]
    cidade = request.form["cidade"]
    uf = request.form["estado"]
    
    EditarPerfil(id_user=current_user.id, nome=nome, sobrenome=sobrenome, numero_telefone=numero_telefone, endereco=endereco, cep=cep, cidade=cidade, uf=uf)

    #definindo rota de onde ficara salvo a img
    id_user = current_user.id
    upload_path = os.environ["UPLOAD_PATHA"]
    timestamp = time.time()
    imagem = request.files['picture__input']
    imagem.save(f'uploads/perfilUser-{id_user}.jpg')
    #Fim Image
         
    return redirect('/perfil')

# <---------------------- Rotas salvar imagem perfil ---------------------->
    
#Foto para perfil 
@blueprint.route('uploads/<nome_arquivo>')
@login_required
def image(nome_arquivo):
    upload_path = os.environ["UPLOAD_PATHA"]
    upload_path = f'../{upload_path}'
    print(upload_path)
    return send_from_directory(upload_path, nome_arquivo)# diretorio - arquivo

# <----------------------------- Rotas Perfil ----------------------------->

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