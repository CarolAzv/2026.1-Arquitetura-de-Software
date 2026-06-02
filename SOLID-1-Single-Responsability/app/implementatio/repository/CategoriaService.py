from ICategoriaService import ICategoriaService
from CategoriaDAO import CategoriaDAO

class CategoriaService(ICategoriaService):
    def __init__(self, dao: CategoriaDAO = None):
        self._dao = dao or CategoriaDAO()
 
 
    def validar(self, categoria, checar_id=False):
        erros = []
 
        if checar_id:
            if not getattr(categoria, "id", None):
                erros.append("O campo 'id' é obrigatório para esta operação.")
            elif not isinstance(categoria.id, int) or categoria.id <= 0:
                erros.append("O campo 'id' deve ser um inteiro positivo.")

        nome = getattr(categoria, "nome", None)
 
        if not nome:
            erros.append("O campo 'nome' é obrigatório.")
        elif not isinstance(nome, str):
            erros.append("O campo 'nome' deve ser uma string.")
        elif len(nome.strip()) < 2:
            erros.append("O campo 'nome' deve ter pelo menos 2 caracteres.")
        elif len(nome.strip()) > 255:
            erros.append("O campo 'nome' deve ter no máximo 255 caracteres.")
 
        return erros

 
    def Incluir(self, categoria):
        erros = self.validar(categoria, checar_id=False)
 
        if erros:
            raise ValueError(f"Erro de validação ao incluir categoria: {'; '.join(erros)}")
 
        categoria.nome = categoria.nome.strip()
        novo_id = self._dao.categoriaIncluir(categoria)
 
        if not novo_id:
            raise RuntimeError("Falha ao incluir o categoria no banco de dados.")
 
        return novo_id
 
 
    def Alterar(self, categoria):
        erros = self.validar(categoria, checar_id=True)
 
        if erros:
            raise ValueError(f"Erro de validação ao alterar categoria: {'; '.join(erros)}")
 
        existente = self._dao.categoriaObter_por_id(categoria.id)
 
        if not existente:
            raise LookupError(f"categoria com id={categoria.id} não encontrado.")
 
        categoria.nome = categoria.nome.strip()
        alterar = self._dao.categoriaAlterar(categoria)
 
        if not alterar:
            raise RuntimeError("Nenhum registro foi alterado no banco de dados.")
 
        return alterar
 
 
    def Excluir(self, categoria):
        if not getattr(categoria, "id", None):
            raise ValueError("O campo 'id' é obrigatório para excluir um categoria.")
 
        praRemover = self._dao.categoriaObter_por_id(categoria.id)
 
        if not praRemover:
            raise LookupError(f"categoria com id={categoria.id} não encontrado.")
 
        self._dao.categoriaExcluir(categoria)
 
        return "Item excluído com sucesso."
 
    def Obter_por_id(self, id):
        if not id:
            raise ValueError("O campo 'id' é obrigatório.")
 
        categoria = self._dao.categoriaObter_por_id(id)
 
        if not categoria:
            raise LookupError(f"Categoria com id={id} não encontrado.")
 
        return categoria
 
 
    def Listar(self):
        return self._dao.categoriaListar()
 