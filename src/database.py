import os 
import psycopg2
from dotenv import load_dotenv

# Carrega as variaveis do arquivo .env
load_dotenv()

# Conexão com o banco de dados
def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection

# Executa as querys
def execute_query(query: str, params: tuple = None) -> list[dict]:
    
    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            
            columns = [col.name for col in cursor.description]
            
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows] 
    finally:
        connection.close()
        
# Executa uma query de escrita
def execute_write(query: str, params: tuple = None) -> None:

    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
        connection.commit()
        
    except Exception as error:
        connection.rollback()
        raise error
    
    finally:
        connection.close()
        
        
        