import sqlalchemy as db
import os
from dotenv import load_dotenv

# É importante chamar load_dotenv() antes de tentar acessar as variáveis de ambiente
load_dotenv()

sqlalchemy_db_url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = None

if sqlalchemy_db_url:
    try:
        engine = db.create_engine(sqlalchemy_db_url)
        print("INFO: Conexão com o banco de dados (engine) criada com sucesso.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao criar a engine do banco de dados: {e}")
else:
    print("ERRO CRÍTICO: SQLALCHEMY_DATABASE_URL não está definida no arquivo .env. A engine não pode ser criada.")