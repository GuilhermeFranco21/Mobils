from apps import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.authentication.models import PaymentMethods, Debts, DebtInstallment

#function que cadastra dividas no banco

def CadastrarDividas(creditor, amount, description, payment_method, number_installments, payment_date, id_user):
    count = 1 # contador
    
    payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
    id_payment_methods = PaymentMethods.query.filter_by(description=payment_method).first().id

    installment_value = int(amount)/int(number_installments)
    
    final_date = payment_date + relativedelta(months=int(number_installments)-1)
    
    print("type: ", id_payment_methods)
    print([creditor, amount, description, payment_method, number_installments, payment_date, final_date, installment_value,])
    
    debt= Debts(creditor=creditor, amount=round(int(amount), 2), description=description, id_payment_methods=id_payment_methods, 
                number_installments=number_installments, installment_value=installment_value, initial_date=payment_date, 
                final_date=final_date, pay=False, id_user=id_user)
    db.session.add(debt)
    db.session.commit()
    
    while count <= int(number_installments):
        payment_date = payment_date + relativedelta(months=1)
        debt_Installment = DebtInstallment(id_debt=debt.id, installment_value=installment_value, payment_date=payment_date, installment_number=count, payed="N", id_user=id_user)
        
        db.session.add(debt_Installment)
        db.session.commit()
        
        count = count + 1


#Funcao para apagar dividas
def DeletarDividas(id):
    # Apaga no DB pelo id
    debt = Debts.query.filter_by(id=id).delete()
    debt_installment = DebtInstallment.query.filter_by(id_debt=id).delete()
    db.session.commit()


