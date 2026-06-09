from app.services.DAO.IProdutoDAO import (produtoIncluir, produtoAlterar, produtoExcluir, produtoObter_por_id, produtoListar, )

class IProdutoService:

    def validar(self, produto):
        erros = []

        if not produto.nome:
            erros.append("O campo 'nome' é obrigatório.")
        elif not isinstance(produto.nome, str):
            erros.append("O campo 'nome' deve ser uma string.")
        elif len(produto.nome.strip()) < 2:
            erros.append("O campo 'nome' deve ter pelo menos 2 caracteres.")
        elif len(produto.nome.strip()) > 255:
            erros.append("O campo 'nome' deve ter no máximo 255 caracteres.")

        return erros


    def Incluir(self, produto):
        erros = self.validar(produto, checar_id=False)

        if erros:
            raise ValueError(f"Erro de validação ao incluir produto: {'; '.join(erros)}")

        produto.nome = produto.nome.strip()
        novo_id = produtoIncluir(produto)
        
        if not novo_id:
            raise RuntimeError("Falha ao incluir o produto no banco de dados.")

        return novo_id


    def Alterar(self, produto):
        erros = self.validar(produto, checar_id=True)

        if erros:
            raise ValueError(f"Erro de validação ao alterar produto: {'; '.join(erros)}")

        existente = produtoObter_por_id(produto.id)

        if not existente:
            raise LookupError(f"Produto com id={produto.id} não encontrado.")

        produto.nome = produto.nome.strip()
        alterar = produtoAlterar(produto)

        if not alterar:
            raise RuntimeError("Nenhum registro foi alterado no banco de dados.")

        return alterar


    def Excluir(self, produto):
        if not produto.id:
            raise ValueError("Não existe um produto com esse id.")

        praRemover = produtoObter_por_id(produto.id)

        if not praRemover:
            raise LookupError(f"Produto com id={produto.id} não encontrado.")

        produtoExcluir(produto)

        mensagem = "Item excluido com sucesso"

        return mensagem


    def Obter_por_id(self, id):
        if not id:
            raise ValueError("O campo 'id' é obrigatório.")

        produto = produtoObter_por_id(id)

        if not produto:
            raise LookupError(f"Produto com id={id} não encontrado.")

        return produto


    def Listar(self):
        return produtoListar()