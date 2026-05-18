import dados.py

import os
import glob
import pandas as pd
from enum import IntEnum


chunkSize = 100000 # Quantidade de linhas a serem lidas por vez
inputFolder = './CSV/'
targetTable = 'tabela_geral'

def transformData(df):
    return df

csvFiles = glob.glob(os.path.join(inputFolder, "*.csv"))

print(f"{len(csvFiles)} arquivos CSV encontrados.")

class aa(IntEnum):
    TP_NOT = 0
    ID_AGRAVO = 1
    DT_NOTIFIC = 2
    SEM_NOT = 3
    NU_ANO = 4
    SG_UF_NOT = 5
    ID_MUNICIP = 6
    ID_REGIONA = 7
    ID_UNIDADE = 8
    DT_SIN_PRI = 9
    SEM_PRI = 10
    ANO_NASC = 11
    NU_IDADE_N = 12
    CS_SEXO = 13
    CS_GESTANT = 14
    CS_RACA = 15
    CS_ESCOL_N = 16
    SG_UF = 17
    ID_MN_RESI = 18
    ID_RG_RESI = 19
    ID_PAIS = 20
    DT_INVEST = 21
    ID_OCUPA_N = 22
    FEBRE = 23
    MIALGIA = 24
    CEFALEIA = 25
    EXANTEMA = 26
    VOMITO = 27
    NAUSEA = 28
    DOR_COSTAS = 29
    CONJUNTVIT = 30
    ARTRITE = 31
    ARTRALGIA = 32
    PETEQUIA_N = 33
    LEUCOPENIA = 34
    LACO = 35
    DOR_RETRO = 36
    DIABETES = 37
    HEMATOLOG = 38
    HEPATOPAT = 39
    RENAL = 40
    HIPERTENSA = 41
    ACIDO_PEPT = 42
    AUTO_IMUNE = 43
    DT_CHIK_S1 = 44
    DT_CHIK_S2 = 45
    DT_PRNT = 46
    RES_CHIKS1 = 47
    RES_CHIKS2 = 48
    RESUL_PRNT = 49
    DT_SORO = 50
    RESUL_SORO = 51
    DT_NS1 = 52
    RESUL_NS1 = 53
    DT_VIRAL = 54
    RESUL_VI_N = 55
    DT_PCR = 56
    RESUL_PCR_ = 57
    SOROTIPO = 58
    HISTOPA_N = 59
    IMUNOH_N = 60
    HOSPITALIZ = 61
    DT_INTERNA = 62
    UF = 63
    MUNICIPIO = 64
    TPAUTOCTO = 65
    COUFINF = 66
    COPAISINF = 67
    COMUNINF = 68
    CLASSI_FIN = 69
    CRITERIO = 70
    DOENCA_TRA = 71
    CLINC_CHIK = 72
    EVOLUCAO = 73
    DT_OBITO = 74
    DT_ENCERRA = 75
    ALRM_HIPOT = 76
    ALRM_PLAQ = 77
    ALRM_VOM = 78
    ALRM_SANG = 79
    ALRM_HEMAT = 80
    ALRM_ABDOM = 81
    ALRM_LETAR = 82
    ALRM_HEPAT = 83
    ALRM_LIQ = 84
    DT_ALRM = 85
    GRAV_PULSO = 86
    GRAV_CONV = 87
    GRAV_ENCH = 88
    GRAV_INSUF = 89
    GRAV_TAQUI = 90
    GRAV_EXTRE = 91
    GRAV_HIPOT = 92
    GRAV_HEMAT = 93
    GRAV_MELEN = 94
    GRAV_METRO = 95
    GRAV_SANG = 96
    GRAV_AST = 97
    GRAV_MIOC = 98
    GRAV_CONSC = 99
    GRAV_ORGAO = 100
    DT_GRAV = 101
    MANI_HEMOR = 102
    EPISTAXE = 103
    GENGIVO = 104
    METRO = 105
    PETEQUIAS = 106
    HEMATURA = 107
    SANGRAM = 108
    LACO_N = 109
    PLASMATICO = 110
    EVIDENCIA = 111
    PLAQ_MENOR = 112
    CON_FHD = 113
    COMPLICA = 114
    TP_SISTEMA = 115
    NDUPLIC_N = 116
    DT_DIGITA = 117
    CS_FLXRET = 118
    FLXRECEBI = 119
    MIGRADO_W = 120

columnsIndices = [1, 2, 3, 4, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48, 49, 1, 2, 52, 62, 63, 64, 65, 66, 67, 69, 70, 71, 72, 73, 74, 75]


for value in columnsIndices:
    print(f"{aa(value).name}, ", end="")

for filePath in csvFiles:
    fileName = os.path.basename(filePath)

    # Exporta o nome e número de todas as colunas
    # print(dict(enumerate(pd.read_csv(filePath, nrows=1).columns)))
    break