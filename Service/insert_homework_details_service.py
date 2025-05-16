
from Repository.db_operations import inser_data,fetch_multiple_rows,fetch_single_row
from Utilities.custom_exceptions import BadRequestException,CustomAPIException
from Utilities.prompt import plan_generatorPrompt
import logging
logging.basicConfig(level=logging.INFO)
from Models.llm import llm_call
import json

def process_insert_home_work_details(params):
    try:
        logging.info("start of process_insert_home_work_details function")
        student_id = params.get("student_id").strip()
        subject_details = params.get("subject_details")

        hours_query="select no_of_hours_to_study from student_details where student_id=%s"
        hours_query_value=(student_id,)
        hours_to_study=fetch_single_row(hours_query,hours_query_value)


        subject_ids = list({item['subject_id'] for item in subject_details})
        difficulty_ids = list({item['subject_difficulty_level'] for item in subject_details})

        # Fetch subject names
        subject_query = """
            SELECT id, subject_name FROM subjects
            WHERE id = ANY(%s);
        """
        # making a dict with id:subject_name format
        subject_rows = fetch_multiple_rows(subject_query, (subject_ids,))
        subject_map = {row[0]: row[1] for row in subject_rows}

        # Fetch difficulty level names
        difficulty_query = """
            SELECT id, difficut_levels FROM subject_difficulty
            WHERE id = ANY(%s);
        """
        difficulty_rows = fetch_multiple_rows(difficulty_query, (difficulty_ids,))
        difficulty_map = {row[0]: row[1] for row in difficulty_rows}

        # Build response
        updated_subject_details = []
        for item in subject_details:
            subject_name = subject_map.get(item['subject_id'], "Unknown")
            difficulty_name = difficulty_map.get(item['subject_difficulty_level'], "Unknown")

            updated_subject_details.append({
                "subject_name": subject_name,
                "subject_difficulty": difficulty_name
            })

        homework_input={
            "homework_details":updated_subject_details,
            "no_hours_to_study": hours_to_study
        }
        
        system_prompt,actual_prompt = plan_generatorPrompt(homework_input)

        print(actual_prompt,"--this is acutual prompt")
        study_plan = llm_call(system_prompt,actual_prompt)
        print(study_plan,"-----------this is study plan")
        # Clean the response
        cleaned_response = study_plan.strip("`").strip()
        if cleaned_response.startswith("json"):
            cleaned_response = cleaned_response[4:].strip()

        # Convert to dictionary
        data_dict = json.loads(cleaned_response)
        

        # insert student-subject mapping details in student_homework table
        mapping_query_base = """
            INSERT INTO student_homework (student_id, subject_id, subject_difficulty_level, allocated_time_to_hw)
            VALUES
        """
        values_placeholder = ",".join(["(%s, %s, %s, %s)" for _ in subject_details])
        mapping_query = mapping_query_base + values_placeholder

        mapping_values = []

        # Create a map from subject name and tag in LLM response to subject_id and difficulty level
        # Assuming subject names in the LLM response match the names from the DB
        llm_subject_schedule = data_dict.get("schedule", [])
        

        # Create reverse maps from subject name/tag back to id
        reverse_subject_map = {v: k for k, v in subject_map.items()}
        reverse_difficulty_map = {v: k for k, v in difficulty_map.items()}


        for item in llm_subject_schedule:
            subject_name = item["subject"]
            difficulty_tag = item["tag"]
            allocated_hour = item["hour"]

            subject_id = reverse_subject_map.get(subject_name)
            difficulty_level_id = reverse_difficulty_map.get(difficulty_tag)

            if subject_id is None or difficulty_level_id is None:
                logging.warning(f"Skipping subject {subject_name} with difficulty {difficulty_tag} due to unmatched mapping.")
                continue

            mapping_values.extend([student_id, subject_id, difficulty_level_id, allocated_hour])
        inser_data(mapping_query, tuple(mapping_values))


        return {"data":"data is inserted successfully","status_code":200}

    except CustomAPIException as ce:
        logging.info("CustomAPIException in process_insert_home_work_details function")
        query = "INSERT INTO error_logs (error, file_name) VALUES (%s, %s);"
        inser_data(query, (str(ce), __name__))
        raise ce
    except Exception as e:
        logging.info("Exception in process_insert_home_work_details function")
        query = "INSERT INTO error_logs (error, file_name) VALUES (%s, %s);"
        inser_data(query, (str(e), __name__))
        raise BadRequestException(str(e))
