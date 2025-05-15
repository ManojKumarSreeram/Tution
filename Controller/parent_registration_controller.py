from Utilities.validate_params import validate_request_body
from Utilities.custom_exceptions import BadRequestException
from Service.parent_registration_service import process_parent_registration_details
from Utilities.custom_exceptions import BadRequestException, CustomAPIException,ForbiddenException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data,fetch_single_row

def validate_parent_registrationDetails(params):
    try:
        logging.info("start of validate_parent_registrationDetails function")
        optional_keys = {}
        missing = validate_request_body(params, optional_keys=optional_keys)
        if not missing:
            query="select * from parent_login where email= %s;"
            email=params.get("email").strip()
            values=(email,)
            is_user_exist=fetch_single_row(query,values)
            if is_user_exist:
                query = """
                        INSERT INTO error_logs (error,file_name)
                        VALUES (%s, %s);
                         """
                values = (f"the user {is_user_exist[1]} {is_user_exist[2]}  with email {is_user_exist[3]} already registered",__name__)
                inser_data(query,values)
                raise ForbiddenException(f"the user {is_user_exist[1]} {is_user_exist[2]}  with email {is_user_exist[3]} already registered")
            else:
                response = process_parent_registration_details(params)
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
        logging.info("customexception in validate_parent_registrationDetails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        # Wrap unknown exceptions into a custom error
        logging.info("unknown exceptions in validate_parent_registrationDetails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))
