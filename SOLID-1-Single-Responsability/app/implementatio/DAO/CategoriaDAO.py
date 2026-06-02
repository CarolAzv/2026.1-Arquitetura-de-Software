from app.services.conexao import Conectar
 

class CategoriaDAO:
    def __init__(self):
        self._conexao = Conectar()
 
 
    def categoriaIncluir(self, categoria):
        return self._conexao.execute( "INSERT INTO Categoria (descricao) VALUES (?)", (categoria.descricao,) ).lastrowid
 
 
    def categoriaAlterar(self, categoria):
        return self._conexao.execute( "UPDATE Categoria SET descricao = ? WHERE id = ?", (categoria.descricao, categoria.id) ).rowcount
 
 
    def categoriaExcluir(self, categoria):
        return self._conexao.execute( "DELETE FROM Categoria WHERE id = ?", (categoria.id,) ).rowcount

 
    def categoriaObter_por_id(self, id):
        return self._conexao.execute( "SELECT * FROM Categoria WHERE id = ?", (id,) ).fetchone()
 
 
    def categoriaListar(self):
        return self._conexao.execute( "SELECT * FROM Categoria" ).fetchall()