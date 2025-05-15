from Service.student_details_service import process_get_Student_details
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_get_studnet_details():
    try:
        logging.info("start of validate_get_studnet_details function")
        response = process_get_Student_details()
        return response

    except CustomAPIException as ce:
        logging.info("customexception in validate_get_studnet_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown exceptions in validate_get_studnet_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))