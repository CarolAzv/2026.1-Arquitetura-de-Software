from decimal import Decimal
from types import SimpleNamespace

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CategoriaForm, ProdutoForm
from .implementatio.repository.CategoriaService import CategoriaService
from .implementatio.repository.ProdutoService import ProdutoService


def categorias(request, acao=None, id=None):
    service = CategoriaService()

    try:
        if acao is None:
            registros = service.Listar()
            return render(request, 'categorias_listar.html', context={'registros': registros})

        elif acao == 'salvar':
            categoriaSalvar(request, service)
            return HttpResponseRedirect(reverse('categorias'))

        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', context={'acao': 'Inclusão', 'form': CategoriaForm()})

        elif acao in ['alterar', 'excluir']:
            registro_dict = categoriaExAlt(id, service)
            acao_exibir = 'Alteração' if acao == 'alterar' else 'Exclusão'
            return render(request, 'categorias_editar.html', context={'acao': acao_exibir, 'form': CategoriaForm(initial=registro_dict)})

        else:
            raise Exception('Ação inválida')

    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def produtos(request, acao=None, id=None):
    service = ProdutoService()

    try:
        if acao is None:
            registros = service.Listar()
            return render(request, 'produtos_listar.html', context={'registros': registros})

        elif acao == 'salvar':
            produtoSalvar(request, service)
            return HttpResponseRedirect(reverse('produtos'))

        elif acao == 'incluir':
            return render(request, 'produtos_editar.html', context={'acao': 'Inclusão', 'form': ProdutoForm()})

        elif acao in ['alterar', 'excluir']:
            registro_dict = produtoAltEx(id, service)
            acao_exibir = 'Alteração' if acao == 'alterar' else 'Exclusão'
            return render(request, 'produtos_editar.html', context={'acao': acao_exibir, 'form': ProdutoForm(initial=registro_dict)})

        else:
            raise Exception('Ação inválida')

    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def home(request):
    return render(request, 'home.html')


# Função auxiliar para obter e converter categoria para dicionário
def categoriaExAlt(id, service):
    registro = service.Obter_por_id(id)
    if registro:
        return {
            'id': registro[0],
            'descricao': registro[1]
        }
    raise Exception(f"Categoria com id {id} não encontrada.")


# Função auxiliar para obter e converter produto para dicionário
def produtoAltEx(id, service):
    registro = service.Obter_por_id(id)
    if registro:
        return {
            'id': registro[0],
            'descricao': registro[1],
            'preco_unitario': registro[2],
            'quantidade_estoque': registro[3],
            'categoria_id': registro[4]
        }
    raise Exception(f"Produto com id {id} não encontrado.")


# Função auxiliar para salvar categoria (inclui ou altera)
def categoriaSalvar(request, service):
    form = CategoriaForm(request.POST)
    acao = request.POST.get('acao', '').strip()
    
    # Se for exclusão, apenas valida se o ID está presente
    if acao == 'Exclusão':
        categoria = SimpleNamespace(
            id=request.POST.get('id'),
            descricao=request.POST.get('descricao', '')
        )
        try:
            categoria.id = int(categoria.id)
            service.Excluir(categoria)
        except (ValueError, TypeError):
            raise Exception("ID inválido para exclusão")
    else:
        # Para inclusão/alteração, valida o formulário normalmente
        if form.is_valid():
            descricao = form.cleaned_data.get('descricao', '').strip()
            if not descricao:
                raise Exception("O campo 'descrição' é obrigatório.")
            
            categoria = SimpleNamespace(
                id=form.cleaned_data.get('id'),
                descricao=descricao
            )
            
            erros = service.Validar(categoria, checar_id=bool(categoria.id))
            if erros:
                raise Exception('; '.join(erros))
            
            if categoria.id:
                service.Alterar(categoria)
            else:
                service.Incluir(categoria)
        else:
            raise Exception("Formulário inválido: " + str(form.errors))


# Função auxiliar para salvar produto (inclui ou altera)
def produtoSalvar(request, service):
    form = ProdutoForm(request.POST)
    acao = request.POST.get('acao', '').strip()
    
    # Se for exclusão, apenas valida se o ID está presente
    if acao == 'Exclusão':
        produto = SimpleNamespace(
            id=request.POST.get('id'),
            descricao=request.POST.get('descricao', ''),
            preco_unitario=request.POST.get('preco_unitario', ''),
            quantidade_estoque=request.POST.get('quantidade_estoque', ''),
            categoria_id=request.POST.get('categoria_id', '')
        )
        try:
            produto.id = int(produto.id)
            service.Excluir(produto)
        except (ValueError, TypeError):
            raise Exception("ID inválido para exclusão")
    else:
        # Para inclusão/alteração, valida o formulário normalmente
        if form.is_valid():
            descricao = form.cleaned_data.get('descricao', '').strip()
            if not descricao:
                raise Exception("O campo 'descrição' é obrigatório.")
            
            preco = form.cleaned_data.get('preco_unitario')
            if not preco:
                raise Exception("O campo 'preço unitário' é obrigatório.")
            
            qtd = form.cleaned_data.get('quantidade_estoque')
            if not qtd:
                raise Exception("O campo 'quantidade em estoque' é obrigatório.")
            
            cat = form.cleaned_data.get('categoria_id')
            if not cat:
                raise Exception("O campo 'categoria' é obrigatório.")
            
            produto = SimpleNamespace(
                id=form.cleaned_data.get('id'),
                descricao=descricao,
                preco_unitario=Decimal(str(preco)),
                quantidade_estoque=qtd,
                categoria_id=cat
            )
            
            erros = service.Validar(produto, checar_id=bool(produto.id))
            if erros:
                raise Exception('; '.join(erros))
            
            if produto.id:
                service.Alterar(produto)
            else:
                service.Incluir(produto)
        else:
            raise Exception("Formulário inválido: " + str(form.errors))