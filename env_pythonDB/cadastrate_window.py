from tkinter import *
from tkinter import ttk
from banco_dados import BancoDados


class CadastrateWindow:
    def __init__(self) -> None:
        self.bd = BancoDados()
        self.janela = Tk()
        self.janela.title("Cadastro de Produtos")
        self.janela.configure(bg="#F5F5F5")
        self.janela.attributes("-fullscreen", False)

        style = ttk.Style(self.janela)
        self.treeview = ttk.Treeview(self.janela, style="mystyle.Treeview")
        style.theme_use("default")
        style.configure("mystyle.Treeview", font=("Arial", 14))
        self.treeview = ttk.Treeview(self.janela, style="mystyle.Treeview", columns=("ID", "NomeProduto", "Descricao", "Preco"), show="headings", height=20)

        self.treeview.heading("ID", text="ID")
        self.treeview.heading("NomeProduto", text="Nome do Produto")
        self.treeview.heading("Descricao", text="Descrição do Produto")
        self.treeview.heading("Preco", text="Preço do Produto")

        self.treeview.column("#0", width=0, stretch=NO)
        self.treeview.column("ID", width=100)
        self.treeview.column("NomeProduto", width=300)
        self.treeview.column("Descricao", width=500)
        self.treeview.column("Preco", width=200)
        self.treeview.grid(row=3, column=0, columnspan=10, stick="NSEW")

        botao_deletar = Button(self.janela, text="Deletar", font=("Arial", 12), command=self.deletar_registro)
        botao_deletar.grid(row=4, column=0, columnspan=10, padx=10, pady=10, stick="NSEW")

        self.treeview.bind("<Double-1>", self.editar_dados)
        menu_barra = Menu(self.janela)
        self.janela.configure(menu=menu_barra)

        menu_arquivo = Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_arquivo.add_command(label="Cadastrar", command=self.cadastrar)
        menu_arquivo.add_command(label="Sair", command=self.janela.destroy)
        self.listar_dados()
        self.janela.mainloop()
    
    def configurar_janela(self, nome_janela, titulo_janela, largura_janela, altura_janela):
        janela = Toplevel(self.janela)
        janela.title(titulo_janela)
        janela.configure(bg="#FFFFFF")
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y ))
        [janela.grid_rowconfigure(i, weight=1) for i in range(5)]
        [janela.grid_columnconfigure(i, weight=1) for i in range(2)]
        self.estilo_borda = {"borderwidth": 2, "relief": "groove"}
        setattr(self, nome_janela, janela)


    #Função para cadastrar o produto
    def cadastrar(self):
        self.configurar_janela("janela_cadastrar", "Cadastrar Produto", 450, 230)

        Label(self.janela_cadastrar, text="Nome do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, stick="W")
        self.nome_produto_cadastrar = Entry(self.janela_cadastrar, font=("Arial", 12), **self.estilo_borda)
        self.nome_produto_cadastrar.grid(row=0, column=1, padx=10, pady=10)
        
        Label(self.janela_cadastrar, text="Descrição do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, stick="W")
        self.descricao_produto_cadastrar = Entry(self.janela_cadastrar, font=("Arial", 12), **self.estilo_borda)
        self.descricao_produto_cadastrar.grid(row=1, column=1, padx=10, pady=10)
        
        Label(self.janela_cadastrar, text="Preço do Produto:", font=("Arial", 12), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, stick="W")
        self.preco_produto_cadastrar = Entry(self.janela_cadastrar, font=("Arial", 12), **self.estilo_borda)
        self.preco_produto_cadastrar.grid(row=2, column=1, padx=10, pady=10)           

        botao_salvar_dados = Button(self.janela_cadastrar, text="Salvar", font=("Arial", 12), command=self.salvar_dados)
        botao_salvar_dados.grid(row=3, column=0, columnspan=2, padx=10, pady=10, stick="NSEW")

        botao_cancelar = Button(self.janela_cadastrar, text="Cancelar", font=("Arial", 12), command=self.janela_cadastrar.destroy)
        botao_cancelar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, stick="NSEW")
    
    def salvar_dados(self):
        self.bd = BancoDados()    
        sql_instruction = f"INSERT INTO Produtos (NomeProduto, Descricao, Preco) Values ('{self.nome_produto_cadastrar.get()}', '{self.descricao_produto_cadastrar.get()}', '{self.preco_produto_cadastrar.get()}')"
        self.bd.insert_query(sql_instruction)       
        self.janela_cadastrar.destroy()

        self.listar_dados()
    
    def listar_dados(self):
        self.bd = BancoDados()
        [self.treeview.delete(item) for item in self.treeview.get_children()]
        sql_instruction = "Select * from Produtos"
        valores = self.bd.execute_query(sql_instruction)
        print(valores)
        [self.treeview.insert("", "end", values=(valor[0], valor[1], valor[2], valor[3])) for valor in valores]

    def editar_dados(self, event):
        self.item_selecionado = self.treeview.selection()[0]
        self.valores_selecionados = self.treeview.item(self.item_selecionado)['values']
        self.configurar_janela("janela_edicao", "Editar Produto", 500, 200)

        Label(self.janela_edicao, text="Nome do Produto:", font=("Arial", 16), bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, stick="W")
        self.nome_produto_edicao = Entry(self.janela_edicao, font=("Arial", 16), **self.estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=self.valores_selecionados[1]))
        self.nome_produto_edicao.grid(row=0, column=1, padx=10, pady=10)
        
        Label(self.janela_edicao, text="Descrição do Produto:", font=("Arial", 16), bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, stick="W")
        self.descricao_produto_edicao = Entry(self.janela_edicao, font=("Arial", 16), **self.estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=self.valores_selecionados[2]))
        self.descricao_produto_edicao.grid(row=1, column=1, padx=10, pady=10)
        
        Label(self.janela_edicao, text="Preço do Produto:", font=("Arial", 16), bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, stick="W")
        self.preco_produto_edicao = Entry(self.janela_edicao, font=("Arial", 16), **self.estilo_borda, bg="#FFFFFF", textvariable=StringVar(value=self.valores_selecionados[3]))
        self.preco_produto_edicao.grid(row=2, column=1, padx=10, pady=10)

        botao_salvar_edicao = Button(self.janela_edicao, text="Alterar", font=("Arial", 12), bg="#008000",fg="#FFFFFF", command=self.salvar_edicao)
        botao_salvar_edicao.grid(row=4, column=0, padx=20, pady=20)
      

    def salvar_edicao(self):
        self.bd = BancoDados()
        nome_produto = self.nome_produto_edicao.get()
        nova_descricao = self.descricao_produto_edicao.get()
        novo_preco = self.preco_produto_edicao.get()
        self.treeview.item(self.item_selecionado, values=(self.valores_selecionados[0], nome_produto, nova_descricao, novo_preco))
        
        sql_instruction = f"UPDATE Produtos SET NomeProduto = '{nome_produto}', Descricao = '{nova_descricao}', Preco = '{novo_preco}' WHERE ID = '{self.valores_selecionados[0]}'"
        self.bd.insert_query(sql_instruction)
        print("Dados alterados com sucesso!")
        
        self.janela_edicao.destroy()
    

    def deletar_registro(self):
        self.bd = BancoDados()
        item_selecionado = self.treeview.focus()
        if item_selecionado:
            id_produto = self.treeview.item(item_selecionado, "values")[0]
            self.bd.delete_id(id_produto)       
            self.listar_dados()

