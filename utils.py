import pandas as pd
from datetime import datetime
import os
from dados import colunasFiltradasNome
import time


def converterIdade(numero):
    if pd.isna(numero):
        return numero
    
    numero_str = str(numero)
    primeiro_caracter = numero_str[0]

    try:
        numero_atual = int(numero_str[1:])
    except:
        return None
    
    # Hora
    if primeiro_caracter == '1': 
        valor_ano = (numero_atual / 24) / 365

    # Dia    
    elif primeiro_caracter == '2':
        valor_ano = (numero_atual / 365)

    # Mes
    elif primeiro_caracter == '3':
        valor_ano = (numero_atual) / 12

    # Ano
    elif primeiro_caracter == '4':
        valor_ano = numero_atual

    try:
        return valor_ano
    
    except:
        print('ERRO: converterIdade | Util.py')
        return None



def conversorData(data, unidade="anos"):
    #Usar lambda ao utilizar apply(lambda x: conversor_data(x, "anos"))
    if pd.isna(data):
        return None
    
    hoje = pd.Timestamp.today()
    delta = hoje - data
    
    if unidade == "dias":
        return delta.days
    
    if unidade == "meses":
        return delta.days / 30
    
    if unidade == "anos":
        return delta.days / 365
    
    return None

def operacoesUtils(op, coluna ,serie, valor, df = None):
    if coluna == 'NU_IDADE_N':
        serie = serie.apply(converterIdade)

    #Operações lógicas
    if op == '==':
        return serie == valor
    
    if op == '>':
        return serie > valor
    
    if op == '<':
        return serie < valor
    
    if op == 'between':
        min, max = valor
        return serie.between(min, max)
    
    if op == '!=':
        return serie != valor
    
    if op == '>=':
        return serie >= valor
    
    if op == '<=':
        return serie <= valor
    
    #Colunas e Operandos
    if isinstance(valor, tuple):
        if op == 'colunas':
            return operacoesUtilsColunas(op, coluna, serie, valor, df)

        operacao_valor, valor_operacao, limite = valor

        #Operandos #Cuidado, SERIE opera com True e False
        if op == '+': #NU_IDADE_N=('+', ('__', 20, 30)) exp, se a idade + 20 == 30
            return serie + valor_operacao == limite
    
        if op == '-':
            return serie + valor_operacao == limite

    raise ValueError('Condição não encotrada')


def operacoesUtilsColunas(op, coluna ,serie, valor, df = None):
    operacao_valor, coluna_do_valor, limite = valor

    if operacao_valor == 'colunas_+_>=':
            return df[coluna_do_valor] + serie >= limite

    if operacao_valor == 'colunas_==': #Comparação linha a linha entre as colunas, Precisam de Index iguais
        return operacoesUtils(op = '==', serie = serie, valor = df[coluna_do_valor]) #Checar se tem utilidade
    
    raise ValueError('Condição não encotrada')


def selecionarCSVs(dir):
    arquivosCSVs = []

    for arquivo in os.listdir(dir):
        if arquivo.endswith('.csv'):
            caminhoCompleto = os.path.join(dir, arquivo)
            arquivosCSVs.append(caminhoCompleto)

    return arquivosCSVs


def contar_linhas(arquivo):
    with open(arquivo, encoding='utf-8') as f:
        return sum(1 for _ in f) - 1  # remove header


def contar_colunas(arquivo, separador):
    with open(arquivo, encoding='utf-8') as f:
        primeira_linha = f.readline()
        if ';' in primeira_linha:
            return len(primeira_linha.strip().split(separador[0]))  # use o separador correto
        if ',' in primeira_linha:
            return len(primeira_linha.strip().split(separador[1]))
        return False


def contar_nulos_por_coluna(arquivo, chunksize=100000):
    contagem = None
    total_linhas = 0
    contador = 0
    tempoFragmento = 0

    for chunk in pd.read_csv(
        arquivo,
        sep=',',
        chunksize=chunksize,
        dtype=str,
        keep_default_na=False
    ):
        tempoInicial = time.perf_counter()

        total_linhas += len(chunk)

        # máscara
        mask = chunk.isin(['\\N', 'DESCONHECIDO',''])

        soma_chunk = mask.sum()

        if contagem is None:
            contagem = soma_chunk
        else:
            contagem += soma_chunk

        tempoFinal = time.perf_counter()
        tempoTotal = tempoFinal - tempoInicial

        print(f"Parte {contador+1} processada em {tempoTotal:.4f} segundos.")
        tempoFragmento += tempoTotal
        print(f"{contador+1} partes processadas em {tempoFragmento:.4f}.\n")

        contador += 1

    percentual = (contagem / total_linhas) * 100

    resultado = pd.DataFrame({
        'nulos': contagem,
        'percentual (%)': percentual
    }).sort_values(by='percentual (%)', ascending=False)

    return resultado


def limpar_nulos(df, colunas):
    return df.dropna(subset=colunas)



def converter_xlsx_to_csv(caminho):
    df = pd.read_excel(caminho)
    # Exporta para CSV
    df.to_csv("./temp/04_relatorio_municipios.csv", index=False)



def main():
    #csv_padrao = selecionarCSVs('./csv/')
    #csv_editado = selecionarCSVs('./csvEditado/')
    #csv = csv_padrao + csv_editado
    converter_xlsx_to_csv("./temp/RELATORIO_DTB_BRASIL_2025_MUNICIPIOS.xls")
    caminhoArquivo = "./csvEditado/temp_editado_1.csv"
   #meucsv = pd.read_csv("./csvEditado/dengue_limpo.csv")
    #print(meucsv.columns.tolist())



if __name__ == '__main__':
    main()
    
    

# count = 0
# for x in csv: #Contar linhas
#     valor_linhas = contar_linhas(x)
#     print(f'{count} = {x} = Tamanho: {valor_linhas}')
#     valor_colunas = contar_colunas(x,[';', ','] )
#     print(f'{count} = {x} = Tamanho: {valor_colunas}')
#     count += 1



# for x in csv_editado: #contar colunas
#         x = './csvEditado/temp.csv'
#         resultado = contar_nulos_por_coluna(x)
#         for coluna, qtd in resultado.items():
#             print(f"{coluna}: {qtd}")



# for csv in csv_padrao: #Verificar as colunas do csv
#         cols = pd.read_csv(csv, nrows=0).columns
        
#         faltando = set(colunasFiltradasNome) - set(cols)
#         extras = set(cols) - set(colunasFiltradasNome)

#         print(csv)
#         print("Faltando:", faltando)
#         print("Extras:", extras)
#         print("-"*50)