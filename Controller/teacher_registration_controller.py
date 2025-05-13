from Utilities.validate_params import validate_request_body
from Utilities.custom_exceptions import BadRequestException
from Service.teacher_registration_service import process_teacher_registration_details
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def validate_teacher_registrationDetails(params):
    try:
        logging.info("start of validate_teacher_registrationDetails function")
        optional_keys = {}
        missing = validate_request_body(params, optional_keys=optional_keys)
        if not missing:
            response = process_teacher_registration_details(params)
            return response
        else:
            raise BadRequestException(f"The required keys {' '.join(missing)} are missing")
    except CustomAPIException as ce:
        # Reraise known custom exception without wrapping
        logging.info("customexception in validate_teacher_registrationDetails function")
        raise ce
    except Exception as e:
        # Wrap unknown exceptions into a custom error
        logging.info("unknown exceptions in validate_teacher_registrationDetails function")
        raise BadRequestException(str(e))
