
from Repository.db_operations import inser_data,fetch_multiple_rows
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_student_regi_master_data():
    try:
        logging.info("start of process_student_regi_master_data function")

        # Educaton Board Details
        edudation_board_query = "select * from education_board"
        edudation_board_result=fetch_multiple_rows(edudation_board_query)

        # Classes Details
        classes_query = "select * from classes"
        classes_result=fetch_multiple_rows(classes_query)

        # access Level Details
        access_levels_query = "select * from access_levels"
        access_levels_result=fetch_multiple_rows(access_levels_query)

        # subject details
        subjects_query = "select * from subjects"
        subjects_result=fetch_multiple_rows(subjects_query)

        # arranging data in json format
        edudation_board_data=list(map(lambda x: {'id': x[0], 'board': x[1]}, edudation_board_result))
        classes_data=list(map(lambda x: {'id': x[0], 'class': x[1]}, classes_result))
        access_levels_data=list(map(lambda x: {'id': x[0], 'premium_type': x[1]}, access_levels_result))
        subjects_data=list(map(lambda x: {'id': x[0], 'class_id': x[1],'subject':x[2],'edu_board_id':x[3]}, subjects_result))

        master_data={
            "education_board_details":edudation_board_data,
            "classe_details":classes_data,
            "access_level_detail":access_levels_data,
            "subject_details":subjects_data
            }
        return {"data":master_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_student_regi_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_student_regi_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))