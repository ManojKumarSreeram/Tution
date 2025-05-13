import psycopg2
from dotenv import load_dotenv
import os
from Utilities.custom_exceptions import InternalServerError
import logging
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)

host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

def connect_db():
    try:
        # Connect to PostgreSQL
        logging.info("start of connect_db function")
        conn = psycopg2.connect(
            host=host,
            database=database,  
            user=user,       
            password=password,
            port=port
        )
        return conn
    except Exception as e:
        logging.info("customexception in connect_db function")
        raise InternalServerError(str(e))

