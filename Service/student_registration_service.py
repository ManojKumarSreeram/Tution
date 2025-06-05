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

def process_student_registration_details(params):
    try:
        logging.info("start of process_student_registration_details function")
        teacher_id=params.get("teacher_id").strip()
        first_name=params.get("first_name").strip()
        last_name=params.get("last_name").strip()
        email=params.get("email").strip()
        password=params.get("password").strip()
        phone_number=params.get("phone_number").strip()
        gender=params.get("gender").strip()

        query = """
                INSERT INTO student_login (teacher_id, first_name, last_name, email, gender, password, phone_number)
                VALUES (%s, %s, %s,%s, %s,%s,%s) RETURNING student_id;
            """
        hashed_password=hash_password(password)
        values = (teacher_id,first_name,last_name,email,gender,hashed_password,phone_number)
        result=inser_data(query,values)
        return {"status":"data is inserted successfully","status_code":200,"data":{"student_id":result}}
    except CustomAPIException as ce:
        logging.info("customexception in process_student_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_student_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))