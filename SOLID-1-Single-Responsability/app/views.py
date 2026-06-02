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