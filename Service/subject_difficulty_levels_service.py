
from Repository.db_operations import inser_data,fetch_multiple_rows
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_subject_difficulty_levels():
    try:
        logging.info("start of process_subject_difficulty_levels function")

        # subject difficulty levels Details
        subject_difficulty_level_query = "select * from subject_difficulty;"
        subject_difficulty_level_result=fetch_multiple_rows(subject_difficulty_level_query)

        # arranging data in json format
        subject_difficulty_level_data=list(map(lambda x: {'id': x[0], 'subject_difficulty': x[1]}, subject_difficulty_level_result))

        sub_diff_level_data={
            "subject_difficulty_level_details":subject_difficulty_level_data,
            }
        return {"data":sub_diff_level_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))