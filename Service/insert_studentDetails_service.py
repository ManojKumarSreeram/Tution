
import bcrypt
from Repository.db_operations import inser_data
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_student_details_insertion(params):
    try:
        logging.info("start of process_student_details_insertion function")
        student_id=params.get("student_id").strip()
        board_id=params.get("board_id")
        class_id=params.get("class_id")
        favourate_subjects=params.get("favourate_subjects")
        toughest_subjects=params.get("toughest_subjects")
        no_of_hours_to_study=params.get("no_of_hours_to_study")
        access_levels_id=params.get("access_levels_id")
        selected_subjects_ids=params.get("selected_subjects_ids")

        # inserting student details
        query = """
                INSERT INTO student_details (student_id,board_id,class_id,favourate_sujects,toughest_sujects,no_of_hours_to_study,access_levels_id)
                VALUES (%s, %s, %s,%s, %s,%s,%s);
            """
        values = (student_id,board_id,class_id,favourate_subjects,toughest_subjects,no_of_hours_to_study,access_levels_id)
        result=inser_data(query,values)

        # insert parent-student mapping details in parent_student table
        mapping_query_base = """
            INSERT INTO student_selected_subjects (student_id, subject_id ) VALUES
        """
        values_placeholder = ",".join(["(%s, %s)" for _ in selected_subjects_ids])
        mapping_query = mapping_query_base + values_placeholder
        mapping_values = []
        for subject_id in selected_subjects_ids:
            mapping_values.extend([student_id, subject_id])  # flatten the list
        inser_data(mapping_query, tuple(mapping_values))

        # update is_details filled status in student_login
        update_query = "UPDATE student_login SET is_details_filled = %s WHERE student_id = %s;"
        update_values = (True, student_id)
        update_result=inser_data(update_query,update_values)

        return {"data":"data is inserted successfully","status_code":200}
    except CustomAPIException as ce:
        logging.info("customexception in process_student_details_insertion function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_student_details_insertion function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))