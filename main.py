from flask import Flask,request, jsonify
from Controller.teacher_registration_controller import validate_teacher_registrationDetails
from Controller.user_login_controller import validate_user_login_details
from Utilities.custom_exceptions import CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)
from Repository.db_operations import inser_data

app = Flask(__name__)

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
        return jsonify({"Error":str(e),"statuscode":e.status_code})
    


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
        return jsonify({"Error":str(e),"statuscode":e.status_code})

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
