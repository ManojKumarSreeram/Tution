

import bcrypt
from Repository.db_operations import inser_data
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime

def process_teacheres_updated_details(params):
    try:
        logging.info("start of process_teacher_registration_details function")
        first_name=params.get("first_name").strip()
        last_name=params.get("last_name").strip()
        email=params.get("email").strip()
        phone_number=params.get("phone_number").strip()
        gender=params.get("gender").strip()
        teacher_id = params.get("teacher_id").strip()

        query = """
                    UPDATE teacher_registration
                    SET first_name = %s,
                        last_name = %s,
                        email = %s,
                        phone_number = %s,
                        gender = %s,
                        modified_at=%s
                    WHERE teacher_id = %s;
                """

        # Get current datetime
        now = datetime.now()

        # Print it in the format: YYYY-MM-DD HH:MM:SS.microseconds
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(formatted_date)
        values = (first_name,last_name,email,phone_number,gender,formatted_date,teacher_id)
        result=inser_data(query,values)
        return {"data":"data is Updated successfully","status_code":200}
    except CustomAPIException as ce:
        logging.info("customexception in process_teacheres_updated_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_teacheres_updated_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))