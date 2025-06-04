

import bcrypt
from Repository.db_operations import inser_data,fetch_single_row
from Utilities.custom_exceptions import BadRequestException,CustomAPIException,ForbiddenException
import logging
logging.basicConfig(level=logging.INFO)
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_MINUTES = 60  # Token valid for 1 hour

# Check password
def check_password(plain_password: str, hashed_password_str: str) -> bool:
    # Convert Postgres-style hex string (like '\\x2432...') to bytes
    if hashed_password_str.startswith("\\x"):
        hashed_password_bytes = bytes.fromhex(hashed_password_str[2:])
    else:
        raise BadRequestException("Invalid hashed password format")
    
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password_bytes)

def create_jwt_token(data: dict) -> str:
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES),
        "iat": datetime.utcnow(),
        "sub": data
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def process_user_login_details(params):
    try:
        logging.info("start of process_user_login_details function")
        email=params.get("email").strip()
        password=params.get("password").strip()
        user_type=params.get('user_type').strip().lower()
        global result 
        if user_type == "teacher":
            query = """
                select password,teacher_id from teacher_registration where email = %s
            """
            values = (email,)
            result=fetch_single_row(query,values)
        elif user_type == "student":
            query = """
                select password,student_id,is_details_filled from student_login where email = %s
            """
            values = (email,)
            result=fetch_single_row(query,values)
        elif user_type == "parent" :
            query = """
                select password,parent_id from parent_login where email = %s
            """
            values = (email,)
            result=fetch_single_row(query,values)
        if result:
            if check_password(password, result[0]):
                user_id = result[1]
                payload_data = {"user_type": user_type, "id": user_id}
                token = create_jwt_token(payload_data)
                if user_type == "student":
                    return {
                    "user_type": user_type,
                    "id": user_id,
                    "token": token,
                    "is_user_details_filled":result[2],
                    "user_type":user_type,
                    "status_code":200
                    }
                return {
                    "user_type": user_type,
                    "id": user_id,
                    "token": token,
                    "user_type":user_type,
                    "status_code":200
                }
            else:
                raise ForbiddenException("Password not matched")
        else:
            raise ForbiddenException("User not registered yet")        
    except CustomAPIException as ce:
        logging.info("customexception in process_user_login_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce
    except Exception as e:
        logging.info("unknown in process_user_login_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        raise BadRequestException(str(e))