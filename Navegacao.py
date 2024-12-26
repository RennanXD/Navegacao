import random as rd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def GerarProblema():
    global mat1
    n = int(entry_tamanho_problema.get())
    
    if n < 10 or n > 30:
        messagebox.showerror("Erro", "O tamanho do problema deve estar entre 10 e 30")
        return
    
    min_c = 10
    max_c = 30
    mat1 = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                mat1[i][j] = rd.randint(min_c, max_c)
    text_problema.delete('1.0', tk.END)
    for row in mat1:
        text_problema.insert(tk.END, ' '.join(map(str, row)) + '\n')

def SolucaoInicial():
    global sol
    n = int(entry_tamanho_problema.get())
    
    if n < 10 or n > 30:
        messagebox.showerror("Erro", "O tamanho do problema deve estar entre 10 e 30")
        return
    
    sol = list(range(n))
    rd.shuffle(sol)
    entry_solucao.delete(0, tk.END)
    entry_solucao.insert(0, ' '.join(map(str, sol)))

def Avalia():
    global sol
    v = 0
    n = len(mat1)
    for i in range(n - 1):
        v += mat1[sol[i]][sol[i + 1]]
    v += mat1[sol[n - 1]][sol[0]]
    label_avaliacao.config(text=f'Avaliação da solução: {v}')
 
# Criar janela principal
root = tk.Tk()
root.title("Problema do Caixeiro Viajante")
 
# Frame e widgets para entrada do tamanho do problema
frame_tamanho_problema = ttk.Frame(root)
frame_tamanho_problema.pack(pady=10)
label_tamanho_problema = ttk.Label(frame_tamanho_problema, text="Tamanho do problema:")
label_tamanho_problema.grid(row=0, column=0)
entry_tamanho_problema = ttk.Entry(frame_tamanho_problema, width=5)
entry_tamanho_problema.grid(row=0, column=1)
 
# Botões para gerar o problema e a solução inicial
frame_botoes = ttk.Frame(root)
frame_botoes.pack(pady=5)
button_gerar_problema = ttk.Button(frame_botoes, text="Gerar Problema", command=GerarProblema)
button_gerar_problema.grid(row=0, column=0, padx=5)
button_solucao_inicial = ttk.Button(frame_botoes, text="Solução Inicial", command=SolucaoInicial)
button_solucao_inicial.grid(row=0, column=1, padx=5)
#button_executar.grid = ttk.Button(frame_botoes, text="Executar", command=Executar)
"""""
#Criando o menu de Opções
frame_opcoes = ttk.Frame(root)
frame_opcoes.pack(pady=10)
frame_opcoes = ttk.OptionMenu(frame_botoes, menu=frame_opcoes)
menu.add_command(label="Subida de Encosta", command=sub_encosta)
menu.add_command(label="Subida de Encosta Altenada", command=sb_alternada)
menu.add_command(label="Tempera Simulada", command=temp_simulada)
"""""

# Widget de texto para exibir o problema gerado
frame_problema = ttk.Frame(root)
frame_problema.pack(pady=10)
label_problema = ttk.Label(frame_problema, text="Problema gerado:")
label_problema.grid(row=0, column=0)
text_problema = tk.Text(frame_problema, height=30, width=70)
text_problema.grid(row=1, column=0)

 
# Entrada para a solução inicial
frame_solucao = ttk.Frame(root)
frame_solucao.pack(pady=10)
label_solucao = ttk.Label(frame_solucao, text="Solução inicial: ")
label_solucao.grid(row=0, column=0)
entry_solucao = ttk.Entry(frame_solucao, width=20)
entry_solucao.grid(row=0, column=1)
 
# Botão para avaliar a solução
frame_botao_avaliar = ttk.Frame(root)
frame_botao_avaliar.pack(pady=5)
button_avaliar = ttk.Button(frame_botao_avaliar, text="Avaliar", command=Avalia)
button_avaliar.pack()
 
# Label para exibir a avaliação da solução
label_avaliacao = ttk.Label(root, text="")
label_avaliacao.pack(pady=10)
 
root.mainloop()