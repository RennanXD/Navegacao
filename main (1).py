import random as rd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# Definições dos Métodos de Otimização

def sub_encosta(solucaoInicial, valorInicial, n, matriz_custo):
    atual = solucaoInicial[:]
    valorAtual = valorInicial
    cidade = list(range(n))
    rd.shuffle(cidade)

    while True:
        indiceCidade = cidade.pop()
        novo, valorNovo = sucessores(atual, valorAtual, n, matriz_custo, indiceCidade)
        if valorNovo >= valorAtual:
            return atual, valorAtual
        atual = novo
        valorAtual = valorNovo

def sub_encosta_alternada(solucaoInicial, valorInicial, n, matriz_custo, tmax):
    atual = solucaoInicial[:]
    valorAtual = valorInicial
    tentativa = 0
    cidade = list(range(n))
    rd.shuffle(cidade)
    while True:
        indiceCidade = cidade.pop()
        novo, valorNovo = sucessores(atual, valorAtual, n, matriz_custo, indiceCidade)
        if valorNovo >= valorAtual:
            if tentativa >= tmax:
                return atual, valorAtual
            else:
                tentativa += 1
        else:
            atual = novo
            valorAtual = valorNovo
            tentativa = 0
            cidade = list(range(n))
            rd.shuffle(cidade)

def tempera_simulada(tempInicial, tempFinal, fatorRedutor, solucaoInicial, valorInicial, n, matriz_custo):
    atual = solucaoInicial[:]
    melhorSolucao = atual
    melhorValor = valorAtual = valorInicial
    temperatura = tempInicial
    while temperatura > tempFinal:
        novo, valorNovo = sucessoresTempera(atual, n, matriz_custo)
        deltaE = valorNovo - valorAtual
        if deltaE < 0 or rd.random() < math.exp(-deltaE / temperatura):
            atual = novo
            valorAtual = valorNovo
            if valorNovo < melhorValor:
                melhorSolucao = atual
                melhorValor = valorNovo
        temperatura *= fatorRedutor
    return melhorSolucao, melhorValor

def sucessores(solucaoAtual, valorAtual, n, matriz_custo, iteracao): 
    melhorSolucao = solucaoAtual[:]
    valorMelhor = valorAtual
    for i in range(n):
        sucessor = solucaoAtual[:]
        sucessor[iteracao], sucessor[i] = sucessor[i], sucessor[iteracao]
        valorSucessor = avalia(sucessor, matriz_custo)
        if valorSucessor < valorMelhor:
            melhorSolucao = sucessor
            valorMelhor = valorSucessor
    return melhorSolucao, valorMelhor

def sucessoresTempera(atual, n, matriz_custo):
    suc = atual[:]
    cidade1, cidade2 = rd.sample(range(n), 2)
    suc[cidade1], suc[cidade2] = suc[cidade2], suc[cidade1]
    valorSolucao = avalia(suc, matriz_custo)
    return suc, valorSolucao

def avalia(rota, matriz_custo):
    custo_total = 0
    n = len(rota)
    for i in range(n - 1):
        custo_total += matriz_custo[rota[i]][rota[i + 1]]
    custo_total += matriz_custo[rota[-1]][rota[0]]
    return custo_total

# Funções para Interface Gráfica

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

def Executar():
    global sol, mat1
    metodo = comboboxMetodo.get()
    if metodo == "Subida de Encosta":
        rotaFinal, valorFinal = sub_encosta(sol, avalia(sol, mat1), len(sol), mat1)
    elif metodo == "Subida de Encosta Alternada":
        tmax = int(entryTmax.get())
        rotaFinal, valorFinal = sub_encosta_alternada(sol, avalia(sol, mat1), len(sol), mat1, tmax)
    elif metodo == "Tempera Simulada":
        tempInicial = int(entryTempInicial.get())
        tempFinal = int(entryTempFinal.get())
        fatorRedutor = float(entryFatorRedutor.get())
        rotaFinal, valorFinal = tempera_simulada(tempInicial, tempFinal, fatorRedutor, sol, avalia(sol, mat1), len(sol), mat1)
    else:
        messagebox.showerror("Erro", "Método não identificado.")
        return

    entry_solucao.delete(0, tk.END)
    entry_solucao.insert(0, ' '.join(map(str, rotaFinal)))
    label_avaliacao.config(text=f'Avaliação da solução: {valorFinal}')

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

# Combobox para seleção do método e botão para execução
comboboxMetodo = ttk.Combobox(frame_botoes, values=["Subida de Encosta", "Subida de Encosta Alternada", "Tempera Simulada"])
comboboxMetodo.grid(row=0, column=2, padx=5)
button_executar = ttk.Button(frame_botoes, text="Executar", command=Executar)
button_executar.grid(row=0, column=3, padx=5)

# Entradas para os parâmetros da Tempera Simulada
frame_parametros_tempera = ttk.Frame(root)
frame_parametros_tempera.pack(pady=10)
label_temp_inicial = ttk.Label(frame_parametros_tempera, text="Temperatura Inicial:")
label_temp_inicial.grid(row=0, column=0, padx=5)
entryTempInicial = ttk.Entry(frame_parametros_tempera, width=10)
entryTempInicial.grid(row=0, column=1, padx=5)

label_temp_final = ttk.Label(frame_parametros_tempera, text="Temperatura Final:")
label_temp_final.grid(row=0, column=2, padx=5)
entryTempFinal = ttk.Entry(frame_parametros_tempera, width=10)
entryTempFinal.grid(row=0, column=3, padx=5)

label_fator_redutor = ttk.Label(frame_parametros_tempera, text="Fator Redutor:")
label_fator_redutor.grid(row=0, column=4, padx=5)
entryFatorRedutor = ttk.Entry(frame_parametros_tempera, width=10)
entryFatorRedutor.grid(row=0, column=5, padx=5)

# Entrada para o parâmetro tmax da Subida de Encosta Alternada
label_tmax = ttk.Label(frame_parametros_tempera, text="Tmax:")
label_tmax.grid(row=0, column=6, padx=5)
entryTmax = ttk.Entry(frame_parametros_tempera, width=10)
entryTmax.grid(row=0, column=7, padx=5)

# Widget de texto para exibir o problema gerado
frame_problema = ttk.Frame(root)
frame_problema.pack(pady=10)
label_problema = ttk.Label(frame_problema, text="Problema gerado:")
label_problema.grid(row=0, column=0)
text_problema = tk.Text(frame_problema, height=30, width=90)
text_problema.grid(row=1, column=0)
 
# Entrada para a solução inicial
frame_solucao = ttk.Frame(root)
frame_solucao.pack(pady=10)
label_solucao = ttk.Label(frame_solucao, text="Solução inicial:")
label_solucao.grid(row=0, column=0)
entry_solucao = ttk.Entry(frame_solucao, width=70)
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