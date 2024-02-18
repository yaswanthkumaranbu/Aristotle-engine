from flask import Flask

# sys.path.append("")

from module.user.userApi import user_api
from module.gai.gaiApi import gai_api, gai_api1


app =Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(gai_api)
app.register_blueprint(gai_api1)

@app.route('/')
def index():
    return 'Hello World!'

app.run(host="0.0.0.0",port=7000)