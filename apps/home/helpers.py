import os
def recupera_imagem(id):
    for nome_arquivo in os.listdir('uploads'):
        if f'perfilUser-{id}' in nome_arquivo:
            return nome_arquivo
    
    return 'imagem-padrao.jpg'

# Mostrar imagem do perfil do usuario
def imgPerfil(id_user):
    id_user=id_user  
    imagemUser = recupera_imagem(id_user)
    return imagemUser
