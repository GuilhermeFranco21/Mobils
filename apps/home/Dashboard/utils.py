from apps import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.authentication.models import PaymentMethods, Debts, DebtInstallment

# Filtro de valor total de dividas do usuario
def DividaTotal(id_user):
    #Calcula total das dividas por usuario. No for ele entra na list e calcula valor por valor e atribui no falorF = valor final
    valorTotalDividas = db.session.query(Debts.amount).filter_by(id_user=id_user).all()
    print("valor total: ", valorTotalDividas)
    valorF = 0
    for iten, valor in enumerate(valorTotalDividas):
        for i, valorI in enumerate(valor):
            valorF = valorF + valorI
        print("valor: ", valorF)
    return valorF

# Contas nao pagas pelo usuario
def ContasNaoPagas(id_user):
    contaNPagas = db.session.query(DebtInstallment).filter(DebtInstallment.payed == 'N').filter_by(id_user=id_user).all()
    valorNPago = 0
    for conta in contaNPagas:
        valorNPago = valorNPago + conta.installment_value
    print("Contas nao pagas: ", valorNPago)
    return valorNPago

# Contas pagas pelo usuario
def ContasPagas(id_user):
    contaPagas = db.session.query(DebtInstallment).filter(DebtInstallment.payed == 'S').filter_by(id_user=id_user).all()
    valorPago = 0
    for row in contaPagas:
        valorPago = valorPago + row.installment_value 
    return valorPago