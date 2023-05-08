import pyodbc


class BancoDados:

    def __init__(self) -> None:
        self.dadosConexao = ("Driver={SQLite3 ODBC Driver};Server=localhost;Database=Projeto_Compras.db")
        self.conexao = pyodbc.connect(self.dadosConexao)
        self.cursor = self.conexao.cursor()

    def execute_query(self, sql_instruction):
        self.cursor.execute(sql_instruction)
        valores = self.cursor.fetchall()
        self.close()

        return valores
    
    def insert_query(self, sql_instruction):
        self.cursor.execute(sql_instruction)
        self.conexao.commit()
        self.close()
    
    def delete_id(self, id):
        try:
            # Executa a operação de delete utilizando a linguagem SQL
            self.cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
            self.conexao.commit()
            print("Produto deletado com sucesso!")
        except Exception as e:
            print("Erro ao deletar produto:", e)
            self.conexao.rollback()
        finally:
            self.conexao.close()

    def close(self):
        self.cursor.close()
        self.conexao.close()
    




# bd = BancoDados()
# sql_instruction = "Select * From Usuarios"
# valores = bd.execute_query(sql_instruction=sql_instruction)
# print(valores)


