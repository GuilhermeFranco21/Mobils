from apps import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.authentication.models import PaymentMethods, Debts

#Registar metodos de pagamento
def registerPaymentMethod(id_user, description):
    payment_method = PaymentMethods(description=description, id_user=id_user)
    db.session.add(payment_method)
    db.session.commit()
