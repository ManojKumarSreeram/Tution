from Repository.db_operations import fetch_multiple_rows, inser_data
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def process_student_selected_subjects(params):
    try:
        logging.info("Start of process_student_selected_subjects function")

        student_id = params.get('student_id').strip()

        # Step 1: Fetch study selected subjects
        query = """ 
            SELECT sss.id, sss.subject_id, s.subject_name 
            FROM student_selected_subjects AS sss 
            JOIN subjects AS s ON sss.subject_id = s.id 
            WHERE sss.student_id = %s and is_active=true;
        """
        selected_subjects = fetch_multiple_rows(query, (student_id,))

        results = [
            {"selected_sub_id": subject_details[0], "sub_id": subject_details[1], "sub_name": subject_details[2]}
            for subject_details in selected_subjects
        ]        

        return {"data": results, "status_code": 200}

    except CustomAPIException as ce:
        logging.exception("CustomException in process_student_selected_subjects")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(ce), __name__))
        raise ce

    except Exception as e:
        logging.exception("Unknown error in process_student_selected_subjects")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(e), __name__))
        raise BadRequestException(str(e))
