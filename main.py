from flask import Flask,request, jsonify
from flask_cors import CORS
from Controller.teacher_registration_controller import validate_teacher_registrationDetails
from Controller.user_login_controller import validate_user_login_details
from Controller.student_regi_master_data_controller import validate_student_regi_master_data
from Controller.subject_difficulty_level_controller import validate_subject_difficulty_levels
from Controller.student_registration_controller import validate_student_registrationDetails
from Controller.parent_registration_controller import validate_parent_registrationDetails
from Controller.student_details_controller import validate_get_studnet_details
from Controller.insert_student_controller import validate_student_details_insertion
from Controller.update_teacher_details_controller import validate_teacheres_updated_details
from Controller.update_parent_details_controller import validate_parent_updated_details
from Controller.update_student_details_controller import validate_student_updated_details
from Controller.insert_homwwork_details_controller import validate_insert_home_work_details
from Controller.update_homework_controller import validate_updated_home_work_details
from Controller.search_engine_controller import validate_search_engine
from Controller.grid_for_parent_controller import validate_grid_for_parent_details
from Controller.get_search_history_controller import validate_get_search_history
from Controller.student_profile_details_controller import validate_student_profile_details
from Controller.teacher_profile_details_controller import validate_teacher_profile_details
from Controller.parent_profile_details_controller import validate_parent_profile_details
from Controller.study_plan_details_controller import validate_study_plan_details
from Controller.student_selected_subjects_controller import validate_student_selected_subjects
from Utilities.custom_exceptions import CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

app = Flask(__name__)
# Enable CORS for all routes and origins (for development only)
CORS(app)

@app.route('/registerTeacher', methods=['POST'])
def register_teacher():
    try :
        logging.info("start of register_teacher function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_teacher_registrationDetails(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in register_teacher function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in register_teacher function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/registerStudent', methods=['POST'])
def register_student():
    try :
        logging.info("start of register_student function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_student_registrationDetails(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in register_student function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in register_student function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/registerParent', methods=['POST'])
def register_parent():
    try :
        logging.info("start of register_parent function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_parent_registrationDetails(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in register_parent function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in register_parent function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})
   
@app.route('/login',methods=['POST'])
def login_user():
    try :
        logging.info("start of login_user function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_user_login_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in login_user function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in login_user function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/updateTeacherDetails', methods=['PUT'])
def update_teacher_deatails():
    try :
        logging.info("start of update_teacher_deatails function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_teacheres_updated_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in update_teacher_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in update_teacher_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/updateStudentDetails', methods=['PUT'])
def update_student_deatails():
    try :
        logging.info("start of update_student_deatails function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_student_updated_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in update_student_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in update_student_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"Error":str(e),"statuscode":400})

@app.route('/updateParentDetails', methods=['PUT'])
def update_parent_deatails():
    try :
        logging.info("start of update_parent_deatails function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_parent_updated_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in update_parent_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in update_parent_deatails function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"Error":str(e),"statuscode":400})

@app.route('/studentRegMasterData',methods=['GET'])
def student_registration_master_data():
    try :
        logging.info("start of student_registration_master_data function")
        result=validate_student_regi_master_data()
        return result
    except CustomAPIException as ce:
        logging.info("customexception in student_registration_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in student_registration_master_data function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/subjectDifficultyLevels',methods=['GET'])
def subject_difficulty_levels():
    try :
        logging.info("start of subject_difficulty_levels function")
        result=validate_subject_difficulty_levels()
        return result
    except CustomAPIException as ce:
        logging.info("customexception in subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in subject_difficulty_levels function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getStudentDetails',methods=['GET'])
def get_student_details():
    try :
        logging.info("start of get_student_details function")
        result=validate_get_studnet_details()
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in get_student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getStudentProfileDetails', methods=['POST'])
def get_student_profile_details():
    try :
        logging.info("start of get_student_profile_details function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_student_profile_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_student_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in get_student_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getTeacherProfileDetails', methods=['POST'])
def get_teacher_profile_details():
    try :
        logging.info("start of get_teacher_profile_details function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_teacher_profile_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in get_teacher_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getParentProfileDetails', methods=['POST'])
def get_parent_profile_details():
    try :
        logging.info("start of get_parent_profile_details function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_parent_profile_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_parent_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in get_parent_profile_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})


@app.route('/insertStudentDetails', methods=['POST'])
def insert_student_details():
    try :
        logging.info("start of insert_student_details function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_student_details_insertion(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in insert_student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in insert_student_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/insertHomeWorkDetails', methods=['POST'])
def insert_home_work_details():
    try :
        logging.info("start of insert_home_work_details function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_insert_home_work_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in insert_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in insert_home_work_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/updateHomeworkrDetails', methods=['PUT'])
def update_homework_details():
    try:
        logging.info("start of update_homework_details function")

        # Extract form fields and file
        homework_status = request.form.get("homework_status")
        homework_id = request.form.get("homework_id")
        comments = request.form.get("comments")
        file_name = request.form.get("file_name")
        file = request.files.get("file")

        if not homework_id or not homework_status:
            return {"data": "homework_id and homework_status are required", "status_code": 401}

        file_content = file.read() if file else None

        # Prepare params dict
        params = {
            "homework_status": homework_status,
            "homework_id": homework_id,
            "comments": comments,
            "file_name": file_name,
            "file_content": file_content
        }

        result = validate_updated_home_work_details(params)
        return result

    except CustomAPIException as ce:
        logging.info("customexception in update_homework_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce), __name__)
        inser_data(query, values)
        raise ce
    except Exception as e:
        logging.info("exception in update_homework_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e), __name__)
        inser_data(query, values)
        return jsonify({"error": str(e), "status_code": 400})

@app.route('/searchEngine', methods=['POST'])
def search_engine():
    try :
        logging.info("start of search_engine function")
        params=request.get_json()
        if not params:
            return {"data":"request body cannot be empty","status_code":401}
        result=validate_search_engine(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in search_engine function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in search_engine function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/gridForParent',methods=['GET'])
def get_grid_for_parent():
    try :
        logging.info("start of get_grid_for_parent function")
        result=validate_grid_for_parent_details()
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_grid_for_parent function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in get_grid_for_parent function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getSearchHistory',methods=['POST'])
def get_search_histoy():
    try :
        logging.info("start of get_search_histoy function")
        params=request.get_json()
        result=validate_get_search_history(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_search_histoy function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in get_search_histoy function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getStudyPlan',methods=['POST'])
def get_study_plan_details():
    try :
        logging.info("start of get_study_plan_details function")
        params=request.get_json()
        result=validate_study_plan_details(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_study_plan_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in get_study_plan_details function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})

@app.route('/getStudentSelectedSubjects',methods=['POST'])
def get_student_selected_subjects():
    try :
        logging.info("start of get_student_selected_subjects function")
        params=request.get_json()
        result=validate_student_selected_subjects(params)
        return result
    except CustomAPIException as ce:
        logging.info("customexception in get_student_selected_subjects function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(ce),__name__)
        inser_data(query,values)
        raise ce       
    except Exception as e :
        logging.info("customexception in get_student_selected_subjects function")
        query = """
                INSERT INTO error_logs (error,file_name)
                VALUES (%s, %s);
            """
        values = (str(e),__name__)
        inser_data(query,values)
        return jsonify({"error":str(e),"status_code":400})


# Central handler for all custom exceptions
@app.errorhandler(CustomAPIException)
def handle_custom_exception(e):
    logging.info("start of handle_custom_exception function")
    response = {
        "error": e.message,
        "status_code":e.status_code
    }
    return jsonify(response), e.status_code



if __name__ == '__main__':
    app.run(debug=False)
