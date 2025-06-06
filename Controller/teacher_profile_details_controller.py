
from Utilities.validate_params import validate_request_body
from Utilities.custom_exceptions import BadRequestException
from Service.teacher_profile_details_service import process_teacher_profile_details
from Utilities.custom_exceptions import BadRequestException, CustomAPIException,ForbiddenException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_teacher_profile_details(params):
    try:
        logging.info("start of validate_teacher_profile_details function")
        optional_keys = {}
        missing = validate_request_body(params, optional_keys=optional_keys)
        if not missing:
            response = process_teacher_profile_details(params)
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
        logging.info("customexception in validate_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        # Wrap unknown exceptions into a custom error
        logging.info("unknown exceptions in validate_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))
