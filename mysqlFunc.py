# Conexão MySQL
# Usuário: 'python'
# Senha: 1234567890

from sqlalchemy import create_engine, Engine, PoolProxiedConnection
from dados import colunasFiltradas, dataIndex
from sqlalchemy.types import Integer, String, Date, Float, Boolean
import pandas as pd

class MySql:
    def __init__(self):
        self.conexao: Engine | None = None
        self.conexaoRaiz: PoolProxiedConnection | None = None

        self.criarConexao()
        self.criarConexaoDireta()


    def criarConexao(self):
        try:
            mysqlConnection = 'mysql+mysqldb://python:1234567890@localhost:3306/dengue'
            conexao = create_engine(mysqlConnection, connect_args={'local_infile': 1})
            self.conexao = conexao
        
        except Exception as e:
            print("Não foi possível conectar com o servidor MySQL.")
            print(e)


    def criarConexaoDireta(self):
        self.conexaoRaiz = self.conexao.raw_connection()


    def enviarCsvMysql(self, arquivoTemp, nomeTabela, fragmento):
        try:
            with self.conexaoRaiz.cursor() as cursor:    
                arquivoTemporarioSeguro = arquivoTemp.replace('\\', '/')
                
                loadSql = f"""
                    LOAD DATA LOCAL INFILE '{arquivoTemporarioSeguro}'
                    INTO TABLE {nomeTabela}
                    FIELDS TERMINATED BY ','
                    ENCLOSED BY '"'
                    LINES TERMINATED BY '\\n'
                    ({', '.join(fragmento.columns)})
                """
                cursor.execute(loadSql)

            self.conexaoRaiz.commit()
            
        finally:
            self.conexaoRaiz.close()


    def criarTabelaVazia(self, nomeTabela, arquivosCsv):
    # Cria um csv vazio apenas para gerar a tabela do MySQL
        if arquivosCsv:
            esquemaTabela = {
                dataIndex.NU_ANO.name: Integer(),
                dataIndex.DT_NS1.name: Date()
            }

            # Le apenas a primeira linha (os nomes)
            emptyCsv = pd.read_csv(arquivosCsv[0], usecols=colunasFiltradas, nrows=0, sep=None, engine='python')
            
            emptyCsv.to_sql(name=nomeTabela, con=self.conexao, if_exists='replace', index=False, dtype=esquemaTabela)
            print("Tabela vazia criada.\n")