import random as rd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# Função de Avaliação (mantida)
def avalia(rota, matriz_custo):
    custo_total = 0
    n = len(rota)
    for i in range(n - 1):
        custo_total += matriz_custo[rota[i]][rota[i + 1]]
    custo_total += matriz_custo[rota[-1]][rota[0]]
    return custo_total

# Função para gerar uma população inicial aleatória
def gerar_populacao(tamanho_populacao, n):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = list(range(n))
        rd.shuffle(individuo)
        populacao.append(individuo)
    return populacao

# Função de seleção (roleta)
def selecionar(populacao, matriz_custo):
    # Avaliar todos os indivíduos da população
    avaliacao = [(individuo, avalia(individuo, matriz_custo)) for individuo in populacao]
    # Ordenar os indivíduos pela sua avaliação (custo)
    avaliacao.sort(key=lambda x: x[1])
    # Selecionar os melhores
    selecionados = avaliacao[:len(avaliacao)//2]  # Seleciona os melhores 50%
    return [individuo for individuo, _ in selecionados]

# Função de cruzamento (crossover)
def cruzamento(pai1, pai2):
    n = len(pai1)
    # Seleciona um ponto de corte aleatório
    ponto_corte = rd.randint(1, n-1)
    filho1 = pai1[:ponto_corte] + [gene for gene in pai2 if gene not in pai1[:ponto_corte]]
    filho2 = pai2[:ponto_corte] + [gene for gene in pai1 if gene not in pai2[:ponto_corte]]
    return filho1, filho2

# Função de mutação
def mutacao(individuo):
    n = len(individuo)
    i, j = rd.sample(range(n), 2)
    individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# Função para aplicar o algoritmo genético
def algoritmo_genetico(tamanho_populacao, n, matriz_custo, geracoes, taxa_mutacao):
    populacao = gerar_populacao(tamanho_populacao, n)
    for _ in range(geracoes):
        # Seleção de indivíduos para cruzamento
        selecionados = selecionar(populacao, matriz_custo)
        
        # Gerar a próxima geração através de cruzamento
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = rd.sample(selecionados, 2)
            filho1, filho2 = cruzamento(pai1, pai2)
            nova_populacao.extend([filho1, filho2])
        
        # Aplicar mutação na população
        for i in range(len(nova_populacao)):
            if rd.random() < taxa_mutacao:
                nova_populacao[i] = mutacao(nova_populacao[i])

        # Atualizar a população
        populacao = nova_populacao
    
    # Avaliar a população final
    avaliacao = [(individuo, avalia(individuo, matriz_custo)) for individuo in populacao]
    avaliacao.sort(key=lambda x: x[1])
    melhor_solucao, melhor_valor = avaliacao[0]
    return melhor_solucao, melhor_valor

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

def ExecutarGenetico():
    global mat1
    metodo = comboboxMetodo.get()
    if metodo == "Algoritmo Genético":
        tamanho_populacao = int(entryTamanhoPopulacao.get())
        geracoes = int(entryGeracoes.get())
        taxa_mutacao = float(entryTaxaMutacao.get())
        rotaFinal, valorFinal = algoritmo_genetico(tamanho_populacao, len(mat1), mat1, geracoes, taxa_mutacao)
        entry_solucao.delete(0, tk.END)
        entry_solucao.insert(0, ' '.join(map(str, rotaFinal)))
        label_avaliacao.config(text=f'Avaliação da solução: {valorFinal}')
        label_solucao_final.config(text=f"Solucao Final {' '.join(map(str,rotaFinal))}")
        label_valor_final.config(text=f"Valor Final: {valorFinal}")
    else:
        messagebox.showerror("Erro", "Método não identificado.")

# Criar janela principal
root = tk.Tk()
root.title("Algoritimo genetico Caxeiro Viajante")

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
comboboxMetodo = ttk.Combobox(frame_botoes, values=["Algoritmo Genético"])
comboboxMetodo.grid(row=0, column=2, padx=5)
button_executar = ttk.Button(frame_botoes, text="Executar", command=ExecutarGenetico)
button_executar.grid(row=0, column=3, padx=5)

# Parâmetros do Algoritmo Genético
frame_parametros_genetico = ttk.Frame(root)
frame_parametros_genetico.pack(pady=10)

label_tamanho_populacao = ttk.Label(frame_parametros_genetico, text="Tamanho População:")
label_tamanho_populacao.grid(row=0, column=0, padx=5)
entryTamanhoPopulacao = ttk.Entry(frame_parametros_genetico, width=10)
entryTamanhoPopulacao.grid(row=0, column=1, padx=5)

label_geracoes = ttk.Label(frame_parametros_genetico, text="Gerações:")
label_geracoes.grid(row=0, column=2, padx=5)
entryGeracoes = ttk.Entry(frame_parametros_genetico, width=10)
entryGeracoes.grid(row=0, column=3, padx=5)

label_taxa_mutacao = ttk.Label(frame_parametros_genetico, text="Taxa Mutação:")
label_taxa_mutacao.grid(row=0, column=4, padx=5)
entryTaxaMutacao = ttk.Entry(frame_parametros_genetico, width=10)
entryTaxaMutacao.grid(row=0, column=5, padx=5)

# Widget de texto para exibir o problema gerado
frame_problema = ttk.Frame(root)
frame_problema.pack(pady=10)
label_problema = ttk.Label(frame_problema, text="Problema gerado:")
label_problema.grid(row=0, column=0)
text_problema = tk.Text(frame_problema, height=10, width=60)
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
label_solucao_final = ttk.Label(root, text="Solução Final: ")
label_solucao_final.pack(pady=5)
label_valor_final = ttk.Label(root, text="Valor Final: ")
label_valor_final.pack(pady=5)

root.mainloop()
