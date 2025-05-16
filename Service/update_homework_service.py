
import bcrypt
from Repository.db_operations import inser_data
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from datetime import datetime



def process_updated_home_work_details(params):
    try:
        logging.info("start of process_updated_home_work_details function")
        homework_status = params.get("homework_status")
        homework_id = params.get("homework_id")
        print(homework_status,homework_id,"--------------")
        query = """
                    UPDATE student_homework
                    SET is_homework_completed = %s,
                        modified_at=%s
                    WHERE id = %s;
                """

        # Get current datetime
        now = datetime.now()

        # Print it in the format: YYYY-MM-DD HH:MM:SS.microseconds
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        values = (homework_status,formatted_date,homework_id)
        result=inser_data(query,values)
        return {"data":"data is Updated successfully","status_code":200}
    except CustomAPIException as ce:
        logging.info("customexception in process_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))