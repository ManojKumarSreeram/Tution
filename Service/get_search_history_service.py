from Repository.db_operations import fetch_multiple_rows, inser_data
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

def process_get_search_history(params):
    try:
        logging.info("Start of process_get_search_history function")
        student_id=params.get('student_id').strip()
        def get_chat_dates(student_id):
            query = """
                SELECT DISTINCT DATE(scs.created_at) AS chat_date
                FROM student_homework_chat_session scs
                WHERE scs.student_id = %s
                ORDER BY chat_date DESC;
            """
            return fetch_multiple_rows(query, (student_id,))

        def get_chat_history_by_date(student_id, chat_date):
            query = """
                SELECT 
                    DATE(scs.created_at) AS chat_date,
                    s.subject_name,
                    sch.role,
                    sch.content,
                    sch.created_at
                FROM student_homework_chat sch
                JOIN student_homework_chat_session scs ON sch.session_id = scs.session_id
                JOIN student_homework shw ON scs.student_homework_id = shw.id
                JOIN subjects s ON shw.subject_id = s.id
                WHERE scs.student_id = %s AND DATE(scs.created_at) = %s
                ORDER BY s.subject_name, sch.created_at ASC;
            """
            return fetch_multiple_rows(query, (student_id, chat_date))

        # Step 1: Get all chat dates for the student
        chat_dates = get_chat_dates(student_id)

        # Step 2: For each date, get grouped history
        grouped_history = {}
        for (chat_date,) in chat_dates:
            chat_date_str = str(chat_date)
            result = get_chat_history_by_date(student_id, chat_date)
            for _, subject_name, role, content, created_at in result:
                if chat_date_str not in grouped_history:
                    grouped_history[chat_date_str] = {}
                if subject_name not in grouped_history[chat_date_str]:
                    grouped_history[chat_date_str][subject_name] = []
                grouped_history[chat_date_str][subject_name].append({
                    "role": role,
                    "content": content,
                    "created_at": str(created_at)
                })

        return {"data": grouped_history, "status_code": 200}

    except CustomAPIException as ce:
        logging.exception("CustomException in process_get_search_history")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(ce), __name__))
        raise ce

    except Exception as e:
        logging.exception("Unknown error in process_get_search_history")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(e), __name__))
        raise BadRequestException(str(e))
