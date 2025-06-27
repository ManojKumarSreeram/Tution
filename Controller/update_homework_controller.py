
from Utilities.validate_params import validate_request_body
from Utilities.custom_exceptions import BadRequestException
from Service.update_homework_service import process_updated_home_work_details
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

def validate_updated_home_work_details(params):
    try:
        logging.info("start of validate_updated_home_work_details function")

        # Only homework_id and homework_status are mandatory
        optional_keys = [ "file_name", "file_content" ]

        missing = validate_request_body(params, optional_keys=optional_keys)

        if not missing:
            response = process_updated_home_work_details(params)
            return response
        else:
            query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
            values = (f"The required keys {' '.join(missing)} are missing", __name__)
            inser_data(query, values)
            raise BadRequestException(f"The required keys {' '.join(missing)} are missing")

    except CustomAPIException as ce:
        logging.info("customexception in validate_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce), __name__)
        inser_data(query, values)
        raise ce
    except Exception as e:
        logging.info("unknown exception in validate_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e), __name__)
        inser_data(query, values)
        raise BadRequestException(str(e))
