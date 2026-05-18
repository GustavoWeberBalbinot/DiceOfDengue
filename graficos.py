import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.ticker as ticker

csv_path = "./csvEditado/dengue_limpo.csv"
tamanhoFragmento = 250000

bins_idade = [0, 4, 14, 24, 34, 44, 54, 64, 74, 84, 200]
mapa_idade = ["0-4", "5-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", "85+"]

mapa_raca = {1: "Branca",2: "Preta",3: "Amarela",4: "Parda",5: "Indigena",9: "Ignorado"}


#TOTAIS

resultado_total_idade = pd.Series(dtype=int)

resultado_genero = pd.Series(dtype=int)

resultado_genero_idade = pd.DataFrame()

resultado_raca = pd.Series(dtype=int)

colunas = ["TP_NOT", "IDADE_MESES", "CS_SEXO", "CS_RACA"]

with pd.read_csv(
    csv_path, chunksize=tamanhoFragmento, usecols=colunas, low_memory=False, sep=',') as leitor:

    for numFragmento, fragmento in enumerate(leitor):
        fragmento = fragmento["TP_NOT"] > 1
        print(numFragmento)

        #Idade
        anos = fragmento["IDADE_MESES"] / 12
        faixas_df_idade = pd.cut(anos,bins=bins_idade,labels=mapa_idade)
        contagem_idade = faixas_df_idade.value_counts()
        resultado_total_idade = resultado_total_idade.add(contagem_idade,fill_value=0)

        #Raças
        
        fragmento["RACA_NOME"] = fragmento["CS_RACA"].map(mapa_raca)
        contagem_raca = fragmento["RACA_NOME"].value_counts()
        resultado_raca = resultado_raca.add(contagem_raca, fill_value=0)

        # Genero
        contagem_genero =  fragmento["CS_SEXO"].value_counts()
        resultado_genero = resultado_genero.add(contagem_genero, fill_value=0)




def grafico_idade(resultado_total_idade):
    plt.figure(figsize=(10,5))
    plt.bar(resultado_total_idade.index,resultado_total_idade.values)
    plt.title("Quantidade de casos por faixa etária")
    plt.xlabel("Faixa etária")
    plt.ylabel("Quantidade")
    plt.axhline(y=500000,linestyle='--')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plt.savefig("./graficos/faixa_etaria.png")
    plt.close()

def grafico_genero(resultado_genero):
    plt.figure(figsize=(10,5))
    plt.bar(resultado_genero.index,resultado_genero.values)
    plt.title("Quantidade de casos por gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Quantidade")
    plt.axhline(y=500000,linestyle='--')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plt.savefig("./graficos/faixa_etaria.png")
    plt.close()

def grafico_raca(resultado_raca):
    plt.figure(figsize=(10,5))
    plt.bar(resultado_raca.index,resultado_raca.values)
    plt.title("Quantidade de casos por raças")
    plt.xlabel("Raças")
    plt.ylabel("Quantidade")
    plt.axhline(y=500000,linestyle='--')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plt.savefig("./graficos/faixa_etaria.png")
    plt.close()




grafico_idade(resultado_total_idade)
grafico_genero(resultado_genero)
grafico_idade(resultado_raca)
















# idades_faixetaria = {
#     1: 0, #0, 4
#     2: 0, #5 - 14
#     3: 0, #15 - 24
#     4: 0, #25 - 34
#     5: 0, #35 - 44
#     6: 0, #45 - 54
#     7: 0, #55 - 64
#     8: 0, #65 - 74
#     9: 0, #75 - 84
#     10: 0, # +85
# }


# def agrupar_idade(idade_meses):
#     idade_ano = idade_meses / 12
#     faixa = -6
#     for x in range(1,11):
#         faixa += 10
#         if idade_ano <= faixa:
#             idades_faixetaria[x] += 1