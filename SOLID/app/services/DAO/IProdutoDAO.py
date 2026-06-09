from app.services.conexao import Conectar

conexao = Conectar()

def produtoIncluir(produto):
    return conexao.execute(
        "INSERT INTO Produto (descricao, preco_unitario, quantidade_estoque, categoria_id) VALUES (?, ?, ?, ?)",
        (produto.descricao, produto.preco_unitario, produto.quantidade_estoque, produto.categoria_id),
    ).lastrowid

def produtoAlterar(produto):
    return conexao.execute(
        "UPDATE Produto SET descricao = ?, preco_unitario = ?, quantidade_estoque = ?, categoria_id = ? WHERE id = ?",
        (produto.descricao, produto.preco_unitario, produto.quantidade_estoque, produto.categoria_id, produto.id),
    ).rowcount

def produtoExcluir(produto):
    return conexao.execute("DELETE FROM Produto WHERE id = ?", (produto.id,)).rowcount

def produtoObter_por_id(id):
    return conexao.execute("SELECT * FROM Produto WHERE id = ?", (id,)).fetchone()

def produtoListar():
    return conexao.execute(
        "SELECT Produto.id, Produto.descricao, Produto.preco_unitario, Produto.quantidade_estoque, Produto.categoria_id, Categoria.descricao AS categoria_nome"
        " FROM Produto JOIN Categoria ON Produto.categoria_id = Categoria.id"
    ).fetchall()