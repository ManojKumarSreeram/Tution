import bcrypt
from Repository.db_operations import inser_data, fetch_single_row
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def hash_password(plain_password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

def process_parent_updated_details(params):
    try:
        logging.info("start of process_parent_updated_details function")

        first_name = params.get("first_name").strip()
        last_name = params.get("last_name").strip()
        email = params.get("email").strip()
        password = params.get("password").strip()
        phone_number = params.get("phone_number").strip()
        gender = params.get("gender").strip()
        parent_id = params.get("parent_id").strip()
        add_student_ids = params.get("add_student_ids")
        remove_student_ids = params.get("remove_student_ids")

        query = """
            UPDATE parent_login
            SET first_name = %s,
                last_name = %s,
                email = %s,
                password = %s,
                phone_number = %s,
                gender = %s,
                modified_at = %s
            WHERE parent_id = %s;
        """

        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S.%f")

        hashed_password = hash_password(password)
        values = (first_name, last_name, email, hashed_password, phone_number, gender, formatted_date, parent_id)
        inser_data(query, values)

        # ------------------------------
        # Add new student mappings
        # ------------------------------
        if add_student_ids:
            for student_id in add_student_ids:
                student_check_query = """
                    SELECT * FROM parent_student
                    WHERE parent_id = %s AND student_id = %s;
                """
                student_check_query_values=(parent_id, student_id)
                existing = fetch_single_row(student_check_query,student_check_query_values )
                
                # inserting new student
                if not existing:
                    new_student_insert_query = """
                        INSERT INTO parent_student (parent_id, student_id)
                        VALUES (%s, %s);
                    """
                    inser_data(new_student_insert_query, student_check_query_values)
                    # making is_active true for previously existing student
                elif not existing[-1] :
                    update_query = """
                    UPDATE parent_student
                    SET is_active = true
                    WHERE parent_id = %s AND student_id = %s;
                     """
                    update_query_values=(parent_id, student_id)
                    inser_data(update_query, update_query_values)

        # ------------------------------
        # Mark removed student mappings as inactive
        # ------------------------------
        print(remove_student_ids,"----------------")
        if remove_student_ids:
            for student_id in remove_student_ids:
                update_query = """
                    UPDATE parent_student
                    SET is_active = false
                    WHERE parent_id = %s AND student_id = %s AND is_active = true;
                """
                update_query_values=(parent_id, student_id)
                inser_data(update_query, update_query_values)

        return {"data": "Data updated successfully", "status_code": 200}

    except CustomAPIException as ce:
        logging.info("custom exception in process_parent_updated_details function")
        log_query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(log_query, (str(ce), __name__))
        raise ce

    except Exception as e:
        logging.info("unknown exception in process_parent_updated_details function")
        log_query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(log_query, (str(e), __name__))
        raise BadRequestException(str(e))
