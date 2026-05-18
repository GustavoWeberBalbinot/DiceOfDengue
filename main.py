from dados import colunasFiltradas, colunasFiltradasNome, dataIndex
import os
import time
import pandas as pd
from utils import *
#from mysqlFunc import *

def selecionarCSVs(dir):
    arquivosCSVs = []

    for arquivo in os.listdir(dir):
        if arquivo.endswith('.csv'):
            caminhoCompleto = os.path.join(dir, arquivo)
            arquivosCSVs.append(caminhoCompleto)

    return arquivosCSVs


# def transformarDados(fragmento, nulo=False, **filtros):
#     """
#     Ele ignora Nulos, se quiser nulos usar nulo=True
#     """
#     # 1. Use 'fragmento.index' instead of 'df_chunk'
#     mascara = pd.Series(True, index=fragmento.index)
    
#     for coluna, condicao in filtros.items():
#         # Safety check: skip if the chunk doesn't have this column
#         if coluna not in fragmento.columns:
#             continue
            
#         # 2. Check if it's a tuple BEFORE trying to unpack it
#         if isinstance(condicao, tuple):
#             operacao = condicao[0]
#             valor = condicao[1]
            
#             if nulo:
#                 cond = operacoesUtils(operacao, coluna, fragmento[coluna], valor, fragmento) | fragmento[coluna].isna()
#             else:
#                 cond = operacoesUtils(operacao, coluna, fragmento[coluna], valor, fragmento)
#         else:
#             # It's a direct equality check (e.g., CS_SEXO='M')
#             if nulo:
#                 cond = (fragmento[coluna] == condicao) | fragmento[coluna].isna()
#             else:
#                 cond = (fragmento[coluna] == condicao)
        
#         # Apply the bitwise AND to the master mask
#         mascara &= cond
    
#     # 3. Return the filtered chunk
#     return fragmento[mascara].copy()



if __name__ == "__main__":
    # Cria a pasta temporária se não existir
    os.makedirs('./csvEditado', exist_ok=True)

    tamanhoFragmento = 250000 # Qtd de linhas por vez
    caminhoArquivo = "./csvs/"    #"./csv/"
    nomeTabela = "tabela_geral"
    arquivoTemporario = './csvEditado/temp.csv'
    caminho_ibge_municipios = "./temp/04_relatorio_municipios.csv"
    arquivoFinal = "./csvEditado/dengue_limpo_1.csv"

    #mysql = MySql()

    #arquivosCSV = selecionarCSVs(caminhoArquivo)
    arquivosCSV = selecionarCSVs(caminhoArquivo)
    print(f"{len(arquivosCSV)} arquivos CSV encontrados.\n")

    #mysql.criarTabelaVazia(nomeTabela, arquivosCSV)
    header_first = True

    if os.path.exists(arquivoTemporario):
        os.remove(arquivoTemporario)

    ibge_municipios = pd.read_csv(caminho_ibge_municipios, dtype=str)
    mapa = dict(zip(ibge_municipios['UF'], ibge_municipios['Nome_UF'])) #dicionário com chave UF e valor Nome_UF

    fatores = {'1': 1/30, '2': 1/4, '3': 1, '4': 12} #utilizado para calcular a idade em meses

    colunas_excecao = ['DT_CHIK_S1', 'DT_OBITO', 'DOENCA_TRA', 'RES_CHIKS2', 'RESUL_PRNT', 'CLINC_CHIK', 'DT_INTERNA', 'MUNICIPIO', 'UF', 'ID_OCUPA_N', 'DT_NS1', 'COUFINF', 'TPAUTOCTO', 'COPAISINF', 'CS_ESCOL_N', 'EVOLUCAO']

    for csv in arquivosCSV:
        nomeArquivo = os.path.basename(csv)

        with pd.read_csv(csv, chunksize=tamanhoFragmento, usecols=colunasFiltradasNome, low_memory=False, sep=',') as leitor:
            tempoFragmento = 0

            for numFragmento, fragmento in enumerate(leitor):
                print(numFragmento)
                tempoInicial = time.perf_counter()

                ## IDADE

                idade_str = fragmento['NU_IDADE_N'].astype(str)

                mask_valido = idade_str.str.len() > 1

                fragmento['IDADE_MESES'] = None

                fragmento.loc[mask_valido, 'IDADE_MESES'] = (
                    idade_str[mask_valido].str[1:].astype(float) *
                    idade_str[mask_valido].str[0].map(fatores)
                )

                fragmento['IDADE_MESES'] = pd.to_numeric(fragmento['IDADE_MESES'], errors='coerce')


                ## UF (apenas do SG_UF_NOT por enquanto)

                fragmento['SG_UF_NOT'] = (fragmento['SG_UF_NOT'].astype(str).str.replace('.0', '', regex=False))
                fragmento['UF_CONVERTIDA'] = fragmento['SG_UF_NOT'].map(mapa).fillna("DESCONHECIDO")


                colunas_verificar = [c for c in fragmento.columns if c not in colunas_excecao] #Quais colunas para verificar, tirando as colunas da colunas_Execao
                mask_invalidos = fragmento[colunas_verificar].isin(['\\N', '', 'DESCONHECIDO']) #Pegando uma máscara dos registros que são "nulos"
                fragmento_limpo = fragmento[~mask_invalidos.any(axis=1)] #Aqui está tirando o nulo. Talvez deixar como NÃO INFORMADO

                fragmento_limpo.to_csv("./csvEditado/dengue_limpo_1.csv", mode='a', index=False, header=header_first, sep=',', na_rep='\\N')

                #fragmento.to_csv(arquivoTemporario, mode='a', index=False, header=header_first, sep=',', na_rep='\\N')
                header_first = False
                
                #mysql.enviarCsvMysql(arquivoTemporario, nomeTabela, fragmento)
                #mysql.enviarCsvMysql(arquivoTemporario, nomeTabela, fragmentoProcessado)
                
                tempoFinal = time.perf_counter()
                tempoTotal = tempoFinal - tempoInicial

                print(f"[{nomeArquivo}] Parte {numFragmento+1} processada em {tempoTotal:.4f} segundos.")
                
                tempoFragmento += tempoTotal
                print(f"{numFragmento+1} partes processadas em {tempoFragmento:.4f}.\n")

        print(f"Finalizado arquivo {nomeArquivo}.\n")

    print("Todos os arquivos foram enviados para o MySQL!")



#Conversores

# ## IDADE

# idade_str = fragmento['NU_IDADE_N'].astype(str)

#                 mask_valido = idade_str.str.len() > 1

#                 fragmento['IDADE_MESES'] = None

#                 fragmento.loc[mask_valido, 'IDADE_MESES'] = (
#                     idade_str[mask_valido].str[1:].astype(float) *
#                     idade_str[mask_valido].str[0].map(fatores)
#                 )

#                 fragmento['IDADE_MESES'] = pd.to_numeric(fragmento['IDADE_MESES'], errors='coerce')


# ## UF (apenas do SG_UF_NOT por enquanto)


#                 fragmento['SG_UF_NOT'] = (fragmento['SG_UF_NOT'].astype(str).str.replace('.0', '', regex=False))
#                 fragmento['UF_CONVERTIDA'] = fragmento['SG_UF_NOT'].map(mapa).fillna("DESCONHECIDO")
                