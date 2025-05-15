from Service.subject_difficulty_levels_service import process_subject_difficulty_levels
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_subject_difficulty_levels():
    try:
        logging.info("start of validate_subject_difficulty_levels function")
        response = process_subject_difficulty_levels()
        return response

    except CustomAPIException as ce:
        logging.info("customexception in validate_subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown exceptions in validate_subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))