
from Service.student_regi_master_data_service import process_student_regi_master_data
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_student_regi_master_data():
    try:
        logging.info("start of validate_student_regi_master_data function")
        response = process_student_regi_master_data()
        return response

    except CustomAPIException as ce:
        logging.info("customexception in validate_student_regi_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown exceptions in validate_student_regi_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))