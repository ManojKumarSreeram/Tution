import bcrypt
from Repository.db_operations import inser_data
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

# Function to hash a plain password
def hash_password(plain_password: str) -> bytes:
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

def process_parent_registration_details(params):
    try:
        logging.info("start of process_parent_registration_details function")
        first_name=params.get("first_name").strip()
        last_name=params.get("last_name").strip()
        email=params.get("email").strip()
        password=params.get("password").strip()
        phone_number=params.get("phone_number").strip()
        gender=params.get("gender").strip()
        student_ids=params.get("student_ids")
        print(student_ids,type(student_ids))

        # Inserting parent detials
        query = """
                INSERT INTO parent_login (first_name, last_name, email,gender, password, phone_number)
                VALUES (%s, %s, %s,%s, %s,%s)
                RETURNING parent_id;
         """
        hashed_password=hash_password(password)
        values = (first_name,last_name,email, gender,hashed_password,phone_number)
        parent_id=inser_data(query,values)
        # Unpack if inser_data returns a tuple
        if isinstance(parent_id, tuple):
            parent_id = parent_id[0]


        # insert parent-student mapping details in parent_student table
        mapping_query_base = """
            INSERT INTO parent_student (parent_id, student_id) VALUES
        """
        values_placeholder = ",".join(["(%s, %s)" for _ in student_ids])
        mapping_query = mapping_query_base + values_placeholder
        mapping_values = []
        for student_id in student_ids:
            mapping_values.extend([parent_id, student_id])  # flatten the list
        inser_data(mapping_query, tuple(mapping_values))
       
        return {"status":"data is inserted successfully","status_code":200,"data":{"parent_id":parent_id}}
    except CustomAPIException as ce:
        logging.info("customexception in process_parent_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_parent_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))