
from Repository.db_operations import inser_data,fetch_single_row
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_teacher_profile_details(params):
    try:
        logging.info("start of process_teacher_profile_details function")
        teacher_id=params.get('teacher_id').strip()
        # student Details
        teacher_details_query = "select teacher_id,first_name, last_name, email,phone_number from teacher_registration where teacher_id = %s and is_active= true;"
        values = (teacher_id,)
        teacher_details_result=fetch_single_row(teacher_details_query,values)

        # arranging data in json format
        teacher_formatted_data={}
        if teacher_details_result:
            teacher_formatted_data = {'id': teacher_details_result[0], 'first_name': teacher_details_result[1],'last_name': teacher_details_result[2],'email': teacher_details_result[3],'phone_number':teacher_details_result[4]}

        
        return {"data":teacher_formatted_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))