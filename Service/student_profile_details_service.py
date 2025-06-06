
from Repository.db_operations import inser_data,fetch_single_row
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_Student_profile_details(params):
    try:
        logging.info("start of process_Student_profile_details function")
        student_id=params.get('student_id').strip()
        # student Details
        student_details_query = "select student_id,first_name, last_name, email,phone_number from student_login where student_id = %s and is_active= true;"
        values = (student_id,)
        student_details_result=fetch_single_row(student_details_query,values)

        # arranging data in json format
        students_formatted_data={}
        if student_details_result:
            students_formatted_data={'id': student_details_result[0], 'first_name': student_details_result[1],'last_name': student_details_result[2],'email': student_details_result[3],'phone_number':student_details_result[4]}

        
        return {"data":students_formatted_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_Student_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_Student_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))