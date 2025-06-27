
from Utilities.validate_params import validate_request_body
from Utilities.custom_exceptions import BadRequestException
from Service.student_selected_subjects_service import process_student_selected_subjects
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_student_selected_subjects(params):
    try:
        logging.info("start of validate_student_selected_subjects function")
        optional_keys = {}
        missing = validate_request_body(params, optional_keys=optional_keys)
        if not missing:
            response = process_student_selected_subjects(params)
            return response
        else:
            query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
            values = (f"The required keys {' '.join(missing)} are missing",__name__)
            inser_data(query,values)
            raise BadRequestException(f"The required keys {' '.join(missing)} are missing")
    except CustomAPIException as ce:
        # Reraise known custom exception without wrapping
        logging.info("customexception in validate_student_selected_subjects function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        # Wrap unknown exceptions into a custom error
        logging.info("unknown exceptions in validate_student_selected_subjects function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))
