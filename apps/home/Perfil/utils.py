from apps import db
from apps.authentication.models import PerfilUser

# Editar Perfil
def EditarPerfil(id_user, nome, sobrenome, numero_telefone, endereco, cep, cidade, uf):
    perfil = PerfilUser.query.filter_by(id_user=id_user).first()
    
    if perfil == None:

        perfil_user = PerfilUser(id_user=id_user, nome=nome, sobrenome=sobrenome, numero_telefone=numero_telefone, endereco=endereco, 
                            cep=cep, cidade=cidade, uf=uf)
        db.session.add(perfil_user)
        db.session.commit()
        print("Saida do id user: ", perfil_user)
    
    else:
         perfil.id_user = id_user
         perfil.nome = nome
         perfil.sobrenome = sobrenome
         perfil.numero_telefone = numero_telefone
         perfil.endereco = endereco
         perfil.cep = cep
         perfil.cidade = cidade
         perfil.uf = uf
         db.session.add(perfil)
         db.session.commit()
