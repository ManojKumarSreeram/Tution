
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
        comments = params.get("comments")
        file_name = params.get("file_name")
        file_content = params.get("file_content")

        logging.info(f"Updating Homework ID: {homework_id}")

        query = """
            UPDATE student_homework
            SET 
                is_homework_completed = %s,
                comments = %s,
                file_name = %s,
                file_content = %s,
                modified_at = %s
            WHERE id = %s;
        """

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        values = (
            homework_status,
            comments,
            file_name,
            file_content,
            now,
            homework_id
        )

        inser_data(query, values)

        return {"data": "Data is updated successfully", "status_code": 200}

    except CustomAPIException as ce:
        logging.info("customexception in process_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce), __name__)
        inser_data(query, values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_updated_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e), __name__)
        inser_data(query, values)
        raise BadRequestException(str(e))
   