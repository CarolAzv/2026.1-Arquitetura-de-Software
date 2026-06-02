from ICategoriaDAO import (categoriaIncluir, categoriaAlterar, categoriaExcluir, categoriaObter_por_id, categoriaListar, )

class ICategoriaService:

    def validar(self, categoria):
        erros = []

        if not categoria.nome:
            erros.append("O campo 'nome' é obrigatório.")
        elif not isinstance(categoria.nome, str):
            erros.append("O campo 'nome' deve ser uma string.")
        elif len(categoria.nome.strip()) < 2:
            erros.append("O campo 'nome' deve ter pelo menos 2 caracteres.")
        elif len(categoria.nome.strip()) > 255:
            erros.append("O campo 'nome' deve ter no máximo 255 caracteres.")

        return erros


    def Incluir(self, categoria):
        erros = self.validar(categoria, checar_id=False)

        if erros:
            raise ValueError(f"Erro de validação ao incluir categoria: {'; '.join(erros)}")

        categoria.nome = categoria.nome.strip()
        novo_id = categoriaIncluir(categoria)
        
        if not novo_id:
            raise RuntimeError("Falha ao incluir o categoria no banco de dados.")

        return novo_id


    def Alterar(self, categoria):
        erros = self.validar(categoria, checar_id=True)

        if erros:
            raise ValueError(f"Erro de validação ao alterar categoria: {'; '.join(erros)}")

        existente = categoriaObter_por_id(categoria.id)

        if not existente:
            raise LookupError(f"categoria com id={categoria.id} não encontrado.")

        categoria.nome = categoria.nome.strip()
        alterar = categoriaAlterar(categoria)

        if not alterar:
            raise RuntimeError("Nenhum registro foi alterado no banco de dados.")

        return alterar


    def Excluir(self, categoria):
        if not categoria.id:
            raise ValueError("Não existe um categoria com esse id.")

        praRemover = categoriaObter_por_id(categoria.id)

        if not praRemover:
            raise LookupError(f"categoria com id={categoria.id} não encontrado.")

        categoriaExcluir(categoria)

        mensagem = "Categoria excluido com sucesso"

        return mensagem


    def Obter_por_id(self, id):
        if not id:
            raise ValueError("O campo 'id' é obrigatório.")

        categoria = categoriaObter_por_id(id)

        if not categoria:
            raise LookupError(f"categoria com id={id} não encontrado.")

        return categoria


    def Listar(self):
        return categoriaListar()