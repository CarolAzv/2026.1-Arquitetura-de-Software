from app.services.repository.IProdutoService import IProdutoService
from app.implementatio.DAO.ProdutoDAO import ProdutoDAO

class ProdutoService(IProdutoService):
    def __init__(self, dao: ProdutoDAO = None):
        self._dao = dao or ProdutoDAO()
 
 
    def Validar(self, produto, checar_id=False):
        erros = []
 
        if checar_id:
            if not getattr(produto, "id", None):
                erros.append("O campo 'id' é obrigatório para esta operação.")
            elif not isinstance(produto.id, int) or produto.id <= 0:
                erros.append("O campo 'id' deve ser um inteiro positivo.")

        descricao = getattr(produto, "descricao", None)
 
        if not descricao:
            erros.append("O campo 'descrição' é obrigatório.")
        elif not isinstance(descricao, str):
            erros.append("O campo 'descrição' deve ser uma string.")
        elif len(descricao.strip()) < 2:
            erros.append("O campo 'descrição' deve ter pelo menos 2 caracteres.")
        elif len(descricao.strip()) > 255:
            erros.append("O campo 'descrição' deve ter no máximo 255 caracteres.")
 
        return erros
 
 
    def Incluir(self, produto):
        erros = self.Validar(produto, checar_id=False)
 
        if erros:
            raise ValueError(f"Erro de validação ao incluir produto: {'; '.join(erros)}")
 
        produto.descricao = produto.descricao.strip()
        novo_id = self._dao.produtoIncluir(produto)
 
        if not novo_id:
            raise RuntimeError("Falha ao incluir o produto no banco de dados.")
 
        return novo_id
 
 
    def Alterar(self, produto):
        erros = self.Validar(produto, checar_id=True)
 
        if erros:
            raise ValueError(f"Erro de validação ao alterar produto: {'; '.join(erros)}")
 
        existente = self._dao.produtoObter_por_id(produto.id)
 
        if not existente:
            raise LookupError(f"Produto com id={produto.id} não encontrado.")
 
        produto.descricao = produto.descricao.strip()
        alterar = self._dao.produtoAlterar(produto)
 
        if not alterar:
            raise RuntimeError("Nenhum registro foi alterado no banco de dados.")
 
        return alterar
 
 
    def Excluir(self, produto):
        if not getattr(produto, "id", None):
            raise ValueError("O campo 'id' é obrigatório para excluir um produto.")
 
        praRemover = self._dao.produtoObter_por_id(produto.id)
 
        if not praRemover:
            raise LookupError(f"Produto com id={produto.id} não encontrado.")
 
        self._dao.produtoExcluir(produto)
 
        return "Item excluído com sucesso."
 
    def Obter_por_id(self, id):
        if not id:
            raise ValueError("O campo 'id' é obrigatório.")
 
        produto = self._dao.produtoObter_por_id(id)
 
        if not produto:
            raise LookupError(f"Produto com id={id} não encontrado.")
 
        return produto
 
 
    def Listar(self):
        return self._dao.produtoListar()
 