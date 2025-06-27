from Repository.db_operations import fetch_multiple_rows, inser_data
from Utilities.custom_exceptions import BadRequestException, CustomAPIException
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)

import base64  # ✅ For encoding binary file content

def process_Study_plan_details(params):
    try:
        logging.info("Start of process_Study_plan_details function")

        student_id = params.get('student_id').strip()

        # Step 1: Fetch study plans
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

            # Step 2: Fetch homework for this plan
            hw_query = """
                SELECT is_homework_completed, file_name, file_content, comments, id
                FROM student_homework
                WHERE student_homework_plan_id = %s
                ORDER BY created_at;
            """
            homework_rows = fetch_multiple_rows(hw_query, (plan_id,))
            print(homework_rows, "------------these are home work rows")

            # Step 3: Merge into schedule
            for idx, item in enumerate(schedule):
                if idx < len(homework_rows):
                    file_content = homework_rows[idx][2]
                    # Convert file_content to base64 if it's not None
                    base64_file = base64.b64encode(file_content).decode('utf-8') if file_content else None

                    item.update({
                        "is_homework_completed": homework_rows[idx][0],
                        "file_name": homework_rows[idx][1],
                        "file_content": base64_file,  # ✅ Send base64 to frontend
                        "comments": homework_rows[idx][3],
                        "homework_id": homework_rows[idx][4]
                    })
                else:
                    item.update({
                        "is_homework_completed": False,
                        "file_name": "",
                        "file_content": None,
                        "comments": "",
                        "homework_id": ""
                    })

            results.append({
                "study_plan_id": plan_id,
                "study_plan": study_plan_data,
                "date": date
            })

        # Step 4: Add dummy plan for today if not found
        today_date = datetime.now().strftime("%d-%m-%Y")
        if not any(r['date'] == today_date for r in results):
            results.insert(0, {
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
