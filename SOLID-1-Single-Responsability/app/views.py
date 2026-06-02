import sys
import sqlite3

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CategoriaForm, ProdutoForm


# Método responsavel por chamar as funções de acordo com necessidade.
def categorias(request, acao=None, id=None):
    '''
    Método responsavel por receber todas as rotas URL do cadastro de Categorias.
    
    De acordo com a "acao" e o "id" informados, esse metodo irá:
      - 'categorias/': Exibir a pagina de listagem
      - 'categorias/incluir/': Exibir a pagina de inclusão
      - 'categorias/alterar/<:id>/': Exibir a pagina de alteração
      - 'categorias/excluir/<:id>/': Exibir a pagina de exclusão
      - 'categorias/salvar/': insere, altera ou exclui um registro
    '''

    try:
        # obtem a conexao com o banco de dados
        conexao = sqlite3.connect('db_solid.sqlite3')
        # comando para não permitir DELETE CASCADE (exclusão em cascata)
        conexao.execute("PRAGMA foreign_keys = ON;") 

        # Listar registros
        # 'categorias/': Exibir a pagina de listagem
        if acao is None:
            registros = categoriaListar(request, conexao)
            return render(request, 'categorias_listar.html', context={'registros': registros})

        
        # Salvar registro
        # 'categorias/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            categoriaSalvar(request, conexao)
            return HttpResponseRedirect( reverse("categorias") )
        
        # inserir registro
        # 'categorias/incluir/': Exibir a pagina de inclusão
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', context={'acao': 'Inclusão', 'form': CategoriaForm() })
        
        # Alterar ou excluir registro
        # 'categorias/alterar/<:id>/': Exibir a pagina de alteração
        # 'categorias/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ['alterar', 'excluir']:
            registro_dict = categoriaExAlt(request, conexao, id, acao)
            return render(request, 'categorias_editar.html', context={'acao': acao, 'form': CategoriaForm(initial=registro_dict) })
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


#--------------------------------------------------------------------------------------------------------------------------#


# Método responsavel por chamar as funções de acordo com necessidade.
def produtos(request, acao=None, id=None):
    '''
    Método responsavel por receber todas as rotas URL do cadastro de Produtos.
    
    De acordo com a "acao" e o "id" informados, esse metodo irá:
      - 'produtos/': Exibir a pagina de listagem
      - 'produtos/incluir/': Exibir a pagina de inclusão
      - 'produtos/alterar/<:id>/': Exibir a pagina de alteração
      - 'produtos/excluir/<:id>/': Exibir a pagina de exclusão
      - 'produtos/salvar/': insere, altera ou exclui um registro
    '''

    try:
        # obtem a conexao com o banco de dados
        conexao = sqlite3.connect('db_solid.sqlite3')
        # comando para não permitir DELETE CASCADE (exclusão em cascata)
        conexao.execute("PRAGMA foreign_keys = ON;") 

        # Listar registros
        # 'produtos/': Exibir a pagina de listagem
        if acao is None:
            registros = produtoListar(request, conexao)
            return render(request, 'produtos_listar.html', context={'registros': registros})
        
        # Salvar registro
        # 'produtos/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            produtoSalvar(request, conexao)
            return HttpResponseRedirect( reverse("produtos") )
        
        # inserir registro
        # 'produtos/incluir/': Exibir a pagina de inclusão
        elif acao == 'incluir':
            return render(request, 'produtos_editar.html', context={'acao': 'Inclusão', 'form': ProdutoForm() })
        
        # Alterar ou excluir registro
        # 'produtos/alterar/<:id>/': Exibir a pagina de alteração
        # 'produtos/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ['alterar', 'excluir']:
            registro_dict = produtoAltEx(request, conexao, id, acao)
            return render(request, 'produtos_editar.html', context={'acao': acao, 'form': ProdutoForm(initial=registro_dict) })
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})
  

#--------------------------------------------------------------------------------------------------------------------------#



# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)