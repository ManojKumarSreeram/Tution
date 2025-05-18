# Service/search_engine.py
from Repository.db_operations import fetch_multiple_rows, inser_data, fetch_single_row
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
from Utilities.prompt import search_query_prompt
from Models.chat_llm import chat_llm
import uuid
import logging
logging.basicConfig(level=logging.INFO)

def process_search_engine(params):
    try:
        logging.info("start of process_search_engine function")
        student_id = params.get("student_id").strip()
        student_homework_id = params.get("student_homework_id")
        new_user_input = params.get("question").strip()

        student_details_query="""
                            SELECT 
                                c.class_name,
                                eb.board_name,
                                s.subject_name
                            FROM 
                                student_homework sh
                            JOIN 
                                subjects s ON sh.subject_id = s.id
                            JOIN 
                                classes c ON s.class_id = c.id
                            JOIN 
                                education_board eb ON s.board_id = eb.id
                            WHERE 
                                sh.student_id = %s
                                AND sh.id = %s;

                            """
        student_details_query_values= (student_id,student_homework_id)
        details=fetch_single_row(student_details_query,student_details_query_values)
        
        standard = details[0]
        education_board=details[1]
        subject = details[2]
        prompt=search_query_prompt(standard,education_board,subject)

        # Step 1: Get or create session
        session_query = """
            SELECT session_id FROM student_homework_chat_session
            WHERE student_homework_id = %s AND student_id = %s
            ORDER BY created_at DESC LIMIT 1;
        """
        session = fetch_single_row(session_query, (student_homework_id, student_id))
        if session:
            session_id = session[0]
        else:
            session_id = str(uuid.uuid4())
            insert_session_query = """
                INSERT INTO student_homework_chat_session (session_id, student_homework_id, student_id)
                VALUES (%s, %s, %s);
            """
            inser_data(insert_session_query, (session_id, student_homework_id, student_id))

        # Step 2: Retrieve chat history for that session
        history_query = """
            SELECT role, content FROM student_homework_chat
            WHERE session_id = %s
            ORDER BY created_at ASC;
        """
        rows = fetch_multiple_rows(history_query, (session_id,))
        history = prompt+[{"role": row[0], "content": row[1]} for row in rows]
        # Step 3: Make LLM call
        updated_history = chat_llm(history, new_user_input)
        # Step 4: Insert new messages (only messages after previous history)
        inserted_count = 0
        if len(updated_history) > len(history):
            new_messages = updated_history[len(history):]
        else:
            new_messages = updated_history[-2:]  # assume user + model
        for message in new_messages:
            insert_chat_query = """
                INSERT INTO student_homework_chat (session_id, role, content)
                VALUES (%s, %s, %s);
            """
            inser_data(insert_chat_query, (session_id, message.role, message.parts[0].text))
            inserted_count += 1

        return {
            "status_code": 200,
            "session_id": session_id,
            "messages": [{"role": m.role, "content": m.parts[0].text} for m in updated_history]
        }

    except CustomAPIException as ce:
        logging.exception("Custom error in process_search_engine")
        raise ce
    except Exception as e:
        logging.exception("Unknown error in process_search_engine")
        raise BadRequestException(str(e))
