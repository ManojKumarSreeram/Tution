
from Repository.db_operations import inser_data,fetch_single_row,fetch_multiple_rows
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_parent_profile_details(params):
    try:
        logging.info("start of process_parent_profile_details function")
        parent_id=params.get('parent_id').strip()
        # parent Details
        parent_details_query = "select parent_id,first_name, last_name, email,phone_number,gender from parent_login where parent_id = %s and is_active= true;"
        values = (parent_id,)
        parent_details_result=fetch_single_row(parent_details_query,values)

        # parent children
        parent_children_query="select student_id from parent_student where parent_id= %s and is_active = true"
        parent_id_value = (parent_id,)
        parent_children_details=fetch_multiple_rows(parent_children_query,parent_id_value)

        # arranging data in json format
        parent_formatted_data = {}
        if parent_details_result:
            parent_formatted_data = {'id': parent_details_result[0], 'first_name': parent_details_result[1],'last_name': parent_details_result[2],'email': parent_details_result[3],'phone_number':parent_details_result[4],'gender':parent_details_result[5]}

        if parent_children_details:
            children_ids=[id[0] for id in parent_children_details]
            parent_formatted_data['student_ids']=children_ids
        
        return {"data":parent_formatted_data,"status_code":200}
        
    except CustomAPIException as ce:
        logging.info("customexception in process_parent_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_parent_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))