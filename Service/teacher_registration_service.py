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

def process_teacher_registration_details(params):
    try:
        logging.info("start of process_teacher_registration_details function")
        first_name=params.get("first_name").strip()
        last_name=params.get("last_name").strip()
        email=params.get("email").strip()
        password=params.get("password").strip()
        phone_number=params.get("phone_number").strip()
        gender=params.get("gender").strip()

        query = """
                INSERT INTO teacher_registration (first_name, last_name, email, password, phone_number,gender)
                VALUES (%s, %s, %s,%s, %s,%s);
            """
        hashed_password=hash_password(password)
        values = (first_name,last_name,email,hashed_password,phone_number,gender)
        result=inser_data(query,values)
        return {"data":"data is inserted successfully","status_code":200}
    except CustomAPIException as ce:
        logging.info("customexception in process_teacher_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_teacher_registration_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))