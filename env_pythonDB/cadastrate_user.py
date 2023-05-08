from tkinter import *
from banco_dados import BancoDados

class InsertUser:

    def __init__(self) -> None:
        self.janela_principal = Tk()
        self.janela_principal.title("Cadastro de Usuário")
        self.janela_principal.configure(bg="#F5F5F5")
        largura_janela = 450
        altura_janela = 300
        largura_tela = self.janela_principal.winfo_screenwidth()
        altura_tela = self.janela_principal.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.janela_principal.geometry('{}x{}+{}+{}'.format(largura_janela, altura_janela, pos_x, pos_y ))
        self.insert_window()

    
    def insert_window(self):
        titulo_lbl = Label(self.janela_principal, text="Cadastro de Usuário", font="Arial 20", fg="blue", bg="#F5F5F5")
        titulo_lbl.grid(row=0, column=0, columnspan=2, pady=20)

        nome_usuario_lbl = Label(self.janela_principal, text="Nome de Usuário", font="Arial 14 bold", bg="#F5F5F5")
        nome_usuario_lbl.grid(row=1, column=0, stick="e")

        senha_usuario_lbl = Label(self.janela_principal, text="Senha", font="Arial 14 bold", bg="#F5F5F5")
        senha_usuario_lbl.grid(row=2, column=0, stick="e")

        self.nome_usuario_entry = Entry(self.janela_principal, font="Arial 14")
        self.nome_usuario_entry.grid(row=1, column=1, pady=10 )

        self.senha_usuario_entry = Entry(self.janela_principal, show="*", font="Arial 14")
        self.senha_usuario_entry.grid(row=2, column=1, pady=10 )

        salvar_btn = Button(self.janela_principal, text="Salvar", font="Arial 14", command=self.insert_user)
        salvar_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

        sair_btn = Button(self.janela_principal, text="Sair", font="Arial 14", command=self.janela_principal.destroy)
        sair_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=10, stick="NSEW")

        [self.janela_principal.grid_rowconfigure(i, weight=1) for i in range(5)]        
        [self.janela_principal.grid_columnconfigure(i, weight=1) for i in range(2)]

        self.janela_principal.mainloop()

    
    def insert_user(self):
        self.bd = BancoDados()
        sql_instruction = f"INSERT INTO Usuarios (Nome, Senha) Values ('{str(self.nome_usuario_entry.get())}', '{str(self.senha_usuario_entry.get())}')"
        self.bd.insert_query(sql_instruction)




