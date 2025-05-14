
from Repository.db_connection import connect_db
from Utilities.custom_exceptions import InternalServerError,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def inser_data(query,values):
    try:   
        logging.info("start of inser_data function")
        conn=connect_db() 
        cur = conn.cursor() 
        # Execute the insert query
        cur.execute(query, values)
        # Commit the transaction
        conn.commit()
        logging.info("Data inserted successfully.")
    except CustomAPIException as ce:
        logging.info("customexception in inser_data function")
        raise ce
    except Exception as e:
        logging.info("customexception in inser_data function")
        raise InternalServerError(str(e))
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def fetch_single_row(query, values=None):
    try:
        logging.info("Start of fetch_single_row function")
        conn = connect_db()
        cur = conn.cursor()
        # Execute the select query
        cur.execute(query, values if values else ())
        row = cur.fetchone()
        logging.info("Data fetched successfully.")
        return row
    except CustomAPIException as ce:
        logging.info("CustomAPIException in fetch_single_row function")
        raise ce
    except Exception as e:
        logging.info("Exception in fetch_single_row function")
        raise InternalServerError(str(e))
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
