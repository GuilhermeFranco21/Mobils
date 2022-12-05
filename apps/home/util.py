import locale
def moeda(request, config="pt_BR.UTF-8"):
    """Recebe um valor e um padrão de locale(ex pt_BR.UTF-8) e devolve o valor formatado"""
    locale.setlocale(locale.LC_ALL, config)
    valor = locale.currency(request, grouping=True, symbol=None)
    return (valor)