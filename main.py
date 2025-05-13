from flask import Flask,request, jsonify
from Controller.teacher_registration_controller import validate_teacher_registrationDetails
from Utilities.custom_exceptions import CustomAPIException
import logging
logging.basicConfig(level=logging.INFO)

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
        raise ce                # Let Flask handle it
    except Exception as e :
        logging.info("customexception in register_teacher function")
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
