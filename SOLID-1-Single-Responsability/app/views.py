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

#----------------------------------------------------------------------------------------------------------#

# Método responsavel por listar
def categoriaListar(request, conexao):
    # define o comando SQL que será executado
    sql = '''
        SELECT  id, 
                descricao
        FROM Categoria 
        ORDER BY descricao
    '''
        
    # cria um cursor(), executa o SELECT informado e traz os todos os registros
    registros = conexao.cursor().execute(sql).fetchall()

    # define a pagina a ser carregada, adicionando os registros das tabelas 
    return registros

# Método responsavel por incluir, excluir e alterar
def categoriaSalvar(request, conexao):
    form_data = request.POST
    acao_form = form_data['acao']

    if acao_form == 'Inclusão':
        sql = f"INSERT INTO Categoria(descricao) VALUES('{form_data['descricao']}')"

    elif acao_form == 'Exclusão':
        sql = f"DELETE FROM Categoria WHERE id = {form_data['id']}"

    else:
        sql = f'''
            UPDATE Categoria 
            SET descricao = '{form_data['descricao']}' 
            WHERE id = {form_data['id']}
        '''

    # cria um cursor() e executa o SQL informado
    conexao.cursor().execute(sql)
    conexao.commit()

    # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
    # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".

# Método responsavel por alterar e excluir.
def categoriaExAlt(request, conexao, id, acao):
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
    # cria um cursor(), executa o SELECT para retornar o registro pelo ID
    registro = conexao.cursor().execute(sql).fetchone()
    registro_dict = {'id': registro[0], 'descricao': registro[1]}

    acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
    acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

    return registro_dict


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

#----------------------------------------------------------------------------------------------------------#

# Método responsavel por listar
def produtoListar(request, conexao):
    # define o comando SQL que será executado
    sql = '''
        SELECT  pro.id,
                pro.descricao, 
                pro.preco_unitario,
                pro.quantidade_estoque,
                pro.categoria_id,
                cat.descricao as 'categoria'
                        
        FROM Produto pro
        INNER JOIN Categoria cat ON cat.id = pro.categoria_id

        ORDER BY pro.descricao
    '''
            
    # cria um cursor(), executa o SELECT informado e traz os todos os registros
    registros = conexao.cursor().execute(sql).fetchall()

    # define a pagina a ser carregada, adicionando os registros das tabelas 
    return registros


# Método responsavel por incluir, alterar e excluir
def produtoSalvar(request, conexao):
    form_data = request.POST
    acao_form = form_data['acao']

    if acao_form == 'Inclusão':
        sql = f'''
            INSERT INTO Produto (
                descricao, 
                preco_unitario, 
                quantidade_estoque, 
                categoria_id
            )
            VALUES(
                '{form_data['descricao']}', 
                {form_data['preco_unitario']}, 
                {form_data['quantidade_estoque']}, 
                {form_data['categoria_id']}
            );
        '''

    elif acao_form == 'Exclusão':
        sql = f"DELETE FROM Produto WHERE id = {form_data['id']}"

    else:
        sql = f'''
            UPDATE Produto 
            SET descricao = '{form_data['descricao']}', 
                preco_unitario = {form_data['preco_unitario']}, 
                quantidade_estoque = {form_data['quantidade_estoque']}, 
                categoria_id = {form_data['categoria_id']} 
            WHERE id = {form_data['id']}
        '''

    # cria um cursor() e executa o SQL informado
    conexao.cursor().execute(sql)
    conexao.commit()

    # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
    # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".


# Método responsavel por alterar e excluir
def produtoAltEx(request, conexao, id, acao):
    # seleciona o registro pelo id informado
    sql = f'''
        SELECT  pro.id,
                pro.descricao, 
                pro.preco_unitario,
                pro.quantidade_estoque,
                pro.categoria_id,
                cat.descricao as 'categoria'
                            
        FROM Produto pro
        INNER JOIN Categoria cat ON cat.id = pro.categoria_id

        WHERE pro.id={id}    
    '''

    # cria um cursor(), executa o SELECT para retornar o registro pelo ID
    registro = conexao.cursor().execute(sql).fetchone()
    registro_dict = {
        'id': registro[0], 
        'descricao': registro[1],
        'preco_unitario': registro[2],
        'quantidade_estoque': registro[3],
        'categoria_id': registro[4],
        'categoria': registro[5],
    }

    acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
    return registro_dict
        
        

#--------------------------------------------------------------------------------------------------------------------------#



# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)