from app.services.conexao import Conectar

conexao = Conectar()

def categoriaIncluir(categoria):
    return conexao.execute("INSERT INTO Categoria (descricao) VALUES (?)", (categoria.descricao,)).lastrowid

def categoriaAlterar(categoria):
    return conexao.execute("UPDATE Categoria SET descricao = ? WHERE id = ?", (categoria.descricao, categoria.id)).rowcount

def categoriaExcluir(categoria):
    return conexao.execute("DELETE FROM Categoria WHERE id = ?", (categoria.id,)).rowcount

def categoriaObter_por_id(id):
    return conexao.execute("SELECT * FROM Categoria WHERE id = ?", (id,)).fetchone()

def categoriaListar():
    return conexao.execute("SELECT * FROM Categoria").fetchall()
