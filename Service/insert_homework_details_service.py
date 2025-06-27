
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

        hours_query = "select no_of_hours_to_study from student_details where student_id=%s"
        hours_query_value = (student_id,)
        hours_to_study = fetch_single_row(hours_query, hours_query_value)

        subject_ids = list({item['subject_id'] for item in subject_details})
        difficulty_ids = list({item['subject_difficulty_level'] for item in subject_details})

        # Fetch subject names
        subject_query = """
            SELECT id, subject_name FROM subjects
            WHERE id = ANY(%s);
        """
        subject_rows = fetch_multiple_rows(subject_query, (subject_ids,))
        subject_map = {row[0]: row[1] for row in subject_rows}

        # Fetch difficulty level names
        difficulty_query = """
            SELECT id, difficut_levels FROM subject_difficulty
            WHERE id = ANY(%s);
        """
        difficulty_rows = fetch_multiple_rows(difficulty_query, (difficulty_ids,))
        difficulty_map = {row[0]: row[1] for row in difficulty_rows}

        updated_subject_details = []
        for item in subject_details:
            subject_name = subject_map.get(item['subject_id'], "Unknown")
            difficulty_name = difficulty_map.get(item['subject_difficulty_level'], "Unknown")

            updated_subject_details.append({
                "subject_name": subject_name,
                "subject_difficulty": difficulty_name
            })

        homework_input = {
            "homework_details": updated_subject_details,
            "no_hours_to_study": hours_to_study
        }

        system_prompt, actual_prompt = plan_generatorPrompt(homework_input)
        study_plan = llm_call(system_prompt, actual_prompt)

        cleaned_response = study_plan.strip("`").strip()
        if cleaned_response.startswith("json"):
            cleaned_response = cleaned_response[4:].strip()

        parsed_llm_response = json.loads(cleaned_response)

        # Insert study plan into DB
        study_plan_query = "INSERT INTO student_homework_plan (study_plan,student_id) VALUES (%s,%s) RETURNING id"
        study_plan_values = (json.dumps(parsed_llm_response),student_id)
        study_plan_id = inser_data(study_plan_query, study_plan_values)


        # Create reverse maps for subject and difficulty
        reverse_subject_map = {v: k for k, v in subject_map.items()}
        reverse_difficulty_map = {v: k for k, v in difficulty_map.items()}

        llm_subject_schedule = parsed_llm_response.get("schedule", [])
        mapping_values = []

        for item in llm_subject_schedule:
            subject_name = item["subject"]
            difficulty_tag = item["tag"]
            allocated_hour = item["hour"]

            subject_id = reverse_subject_map.get(subject_name)
            difficulty_level_id = reverse_difficulty_map.get(difficulty_tag)

            if subject_id is None or difficulty_level_id is None or study_plan_id is None:
                logging.warning(f"Skipping subject {subject_name} with difficulty {difficulty_tag} due to unmatched mapping.")
                continue

            mapping_values.append((student_id, subject_id, difficulty_level_id, allocated_hour, study_plan_id))

        # Final insertion using many=True and single VALUES template
        mapping_query = """
            INSERT INTO student_homework (student_id, subject_id, subject_difficulty_level, allocated_time_to_hw, student_homework_plan_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        inser_data(mapping_query, mapping_values, many=True)

        new_parsed_llm_respones = [
            {
                **item,
                "is_homework_completed": False,
                "file_name": "",
                "file_content": None,
                "comments": ""
            }
            for item in llm_subject_schedule
        ]

        # Optionally return or log the final enriched response
        return {
            "status_code": 200,
            "study_plan_id": study_plan_id,
            "homework_schedule": new_parsed_llm_respones
        }
   

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
