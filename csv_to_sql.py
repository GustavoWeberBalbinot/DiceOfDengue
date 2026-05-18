import pymysql
import pandas as pd

# =============================
# CONFIG
# =============================
HOST = "localhost"
PORT = 3306
USER = "python"
PASSWORD = "1234567890"
DATABASE = "dengue"

CSV_PATH = "./csvEditado/dengue_limpo.csv"
TABELA = "tabela_geral"
CHUNK_SIZE = 5000
DELIMITER = ","


# =============================
# CONEXÃO + CURSOR
# =============================
def conectar_mysql():
    conexao = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        local_infile=True,
        autocommit=False
    )

    cursor = conexao.cursor()
    return conexao, cursor


# =============================
# CRIAR TABELA (DINÂMICO)
# =============================
def criar_tabela(cursor, nome_tabela, colunas):
    colunas_sql = ", ".join([f"`{col}` TEXT" for col in colunas])

    sql = f"""
    CREATE TABLE IF NOT EXISTS {nome_tabela} (
        {colunas_sql}
    )
    """

    cursor.execute(sql)


# =============================
# INSERÇÃO EM LOTE
# =============================
def inserir_lote(cursor, nome_tabela, df):
    cols = list(df.columns)
    colunas_sql = ", ".join([f"`{c}`" for c in cols])
    placeholders = ", ".join(["%s"] * len(cols))

    sql = f"""
        INSERT INTO {nome_tabela} ({colunas_sql})
        VALUES ({placeholders})
    """

    dados = [tuple(x) for x in df.fillna("\\N").values]

    cursor.executemany(sql, dados)


# =============================
# PIPELINE PRINCIPAL
# =============================
def processar_csv():
    conexao, cursor = conectar_mysql()

    try:
        leitor = pd.read_csv(
            CSV_PATH,
            sep=DELIMITER,
            chunksize=CHUNK_SIZE,
            low_memory=False
        )

        primeira = True

        for i, chunk in enumerate(leitor):
            print(f"Processando chunk {i+1}...")

            if primeira:
                criar_tabela(cursor, TABELA, chunk.columns)
                primeira = False

            inserir_lote(cursor, TABELA, chunk)
            conexao.commit()

        print("Finalizado com sucesso.")

    except Exception as e:
        conexao.rollback()
        print("Erro:", e)

    finally:
        cursor.close()
        conexao.close()


# =============================
# EXECUÇÃO
# =============================
if __name__ == "__main__":
    processar_csv()