import sqlite3
from django import forms


# formulario utilizado para edicao de registros de categorias
class CategoriaForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=False, widget=forms.TextInput())

# formulario utilizado para edicao de registros de produtos
class ProdutoForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=False, widget=forms.TextInput())
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=False)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=False)
    categoria_id = forms.ChoiceField(label='Categoria', required=False)

    # construtor do Formulario
    def __init__(self, *args, **kwargs):
            # chama construtor da classe-Pai
            super().__init__(*args, **kwargs)
            # obtem a conexao com o banco de dados
            conexao = sqlite3.connect('db_solid.sqlite3', check_same_thread=False)
            # obtem os registros da tabela Departamentos
            categorias = conexao.cursor().execute('SELECT id, descricao FROM Categoria ORDER BY descricao').fetchall()
            # carrega as categorias no <select> da página usando o ChoiceField
            self.fields['categoria_id'].choices = categorias