from Repository.db_operations import fetch_multiple_rows, inser_data
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def process_Study_plan_details(params):
    try:
        logging.info("Start of process_Study_plan_details function")

        student_id = params.get('student_id').strip()

        # Step 1: Fetch study plans for the student
        query = """
            SELECT id AS study_plan_id, study_plan, created_at
            FROM student_homework_plan
            WHERE student_id = %s
            ORDER BY created_at desc;
        """
        study_plans = fetch_multiple_rows(query, (student_id,))

        results = []

        for plan in study_plans:
            plan_id = plan[0]
            date = plan[2].strftime("%d-%m-%Y") if plan[2] else None
            try:
                study_plan_data = json.loads(plan[1])
            except json.JSONDecodeError:
                logging.warning(f"Invalid JSON in study_plan_id: {plan_id}")
                continue

            schedule = study_plan_data.get("schedule", [])

            # Step 2: Fetch homework records for this plan
            hw_query = """
                SELECT is_homework_completed, file_name, file_content, comments
                FROM student_homework
                WHERE student_homework_plan_id = %s
                ORDER BY created_at;
            """
            homework_rows = fetch_multiple_rows(hw_query, (plan_id,))
            print(homework_rows, "------------these are home work rows")

            # Step 3: Merge data into schedule (index-based match)
            for idx, item in enumerate(schedule):
                if idx < len(homework_rows):
                    item.update({
                        "is_homework_completed": homework_rows[idx][0],
                        "file_name": homework_rows[idx][1],
                        "file_content": homework_rows[idx][2],
                        "comments": homework_rows[idx][3]
                    })
                else:
                    item.update({
                        "is_homework_completed": False,
                        "file_name": "",
                        "file_content": None,
                        "comments": ""
                    })

            results.append({
                "study_plan_id": plan_id,
                "study_plan": study_plan_data,
                "date": date
            })

        # Step 4: Add today's date if not present
        today_date = datetime.now().strftime("%d-%m-%Y")
        if not any(r['date'] == today_date for r in results):
            results.insert(0,{
                "study_plan_id": None,
                "study_plan": {},
                "date": today_date
            })

        return {"data": results, "status_code": 200}

    except CustomAPIException as ce:
        logging.exception("CustomException in process_Study_plan_details")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(ce), __name__))
        raise ce

    except Exception as e:
        logging.exception("Unknown error in process_Study_plan_details")
        query = """
            INSERT INTO error_logs (error, file_name)
            VALUES (%s, %s);
        """
        inser_data(query, (str(e), __name__))
        raise BadRequestException(str(e))
