from flask import Blueprint,request
from flask_cors import CORS , cross_origin
from module.gai.gaiService import GaiService

gai_service = GaiService()
gai_api  = Blueprint('gai_api', __name__)
CORS(gai_api,support_credentails=True )

@gai_api.route("/gai/chat",methods=["GET"])
@cross_origin(support_credentails=True )
def api_chat(): 
    params = request.args.get('q', '')
    data = gai_service.chat_with_gai(params)
    # params = request.get_json(force=True)
    print(data)
    return data

gai_api1  = Blueprint('gai_api1', __name__)
CORS(gai_api1,support_credentails=True )
@gai_api1.route("/gai/hybrid",methods=["GET"])
@cross_origin(support_credentails=True )
def api_chat(): 
    params = request.args.get('q', '')
    data = gai_service.chat_with_gai_hybrid(params)
    # params = request.get_json(force=True)
    print(data)
    return data

