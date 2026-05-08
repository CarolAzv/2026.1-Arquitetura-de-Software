import sys
import sqlite3
from app.services.serviceCategoria import ServiceCateogria
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

# Método responsavel por listar, incluir, alterar e excluir as Categorias.
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
        
        # Listar registros
        # 'categorias/': Exibir a pagina de listagem
        if acao is None:
            
            # carrega os todos os registros
            registros = ServiceCateogria.listarCategoria()

            # define a pagina a ser carregada, adicionando os registros das tabelas 
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # Salvar registro
        # 'categorias/salvar/': insere, altera ou exclui um registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            AAAAAAAA

            # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
            # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
            return HttpResponseRedirect( reverse("categorias") )
        
        # inserir registro
        # 'categorias/incluir/': Exibir a pagina de inclusão
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html',
                           context={'acao': 'Inclusão', 'form': CategoriaForm() })
        
        # Alterar ou excluir registro
        # 'categorias/alterar/<:id>/': Exibir a pagina de alteração
        # 'categorias/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ['alterar', 'excluir']:
            # seleciona o registro pelo id informado
            sql = f'''
                SELECT  id, 
                        descricao 
                FROM Categoria 
                WHERE id={id}
            '''

            # cria um cursor(), executa o SELECT para retornar o registro pelo ID
            registro = conexao.cursor().execute(sql).fetchone()
            registro_dict = {'id': registro[0], 'descricao': registro[1]}

            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'categorias_editar.html', 
                           context={'acao': acao, 'form': CategoriaForm(initial=registro_dict) })
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})