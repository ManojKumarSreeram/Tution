
from Repository.db_operations import inser_data,fetch_multiple_rows
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_grid_for_parent_details():
    try:
        logging.info("start of process_grid_for_parent_details function")

        query = """
            SELECT 
                sl.first_name,
                sl.last_name,
                sl.email,
                sd.*,
                sss.subject_id
            FROM 
                student_login sl
            LEFT JOIN 
                student_details sd ON sl.student_id = sd.student_id AND sd.is_active = true
            LEFT JOIN 
                student_selected_subjects sss ON sl.student_id = sss.student_id AND sss.is_active = true
            WHERE 
                sl.is_active = true;

        """
        student_grid_raw_data = fetch_multiple_rows(query)

        # Define column names in the same order as the SELECT
        columns = [
            "first_name", "last_name", "email",
            "id", "student_id", "board_id", "class_id",
            "favourate_sujects", "toughest_sujects", "no_of_hours_to_study",
            "access_levels_id", "created_at", "modified_at", "is_active",
            "subject_id"
        ]

        student_grid_data = [
            dict(zip(columns, row)) for row in student_grid_raw_data
        ]


        return {"data": student_grid_data, "status_code": 200}

    except CustomAPIException as ce:
        logging.info("customexception in process_grid_for_parent_details function")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        values = (str(ce), __name__)
        inser_data(query, values)
        raise ce

    except Exception as e:
        logging.info("unknown in process_grid_for_parent_details function")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        values = (str(e), __name__)
        inser_data(query, values)
        raise BadRequestException(str(e))
   
