
from Repository.db_operations import inser_data,fetch_multiple_rows
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_get_Student_details():
    try:
        logging.info("start of process_get_Student_details function")

        # student Details
        student_details_query = "select student_id,first_name, last_name, email from student_login where is_active= true;"
        student_details_result=fetch_multiple_rows(student_details_query)

        # arranging data in json format
        students_formatted_data=list(map(lambda x: {'id': x[0], 'first_name': x[1],'last_name': x[2],'email': x[3]}, student_details_result))

        students_data={
            "student_details":students_formatted_data,
            }
        return {"data":students_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_get_Student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_get_Student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))