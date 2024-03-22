from flask import Blueprint
from flask_cors import CORS , cross_origin

user_api  = Blueprint('user_api', __name__)
CORS(user_api,support_credentails=True )

@user_api.route("/user/login",methods=["GET"])
@cross_origin(support_credentails=True )
def api_userLogin():
    data = 'suerlogin'
    return data

