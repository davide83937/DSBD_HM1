from flask import Flask
from UserManagerMicroservice import app

appl = Flask(__name__)
appl.register_blueprint(app)

appl.run(host='0.0.0.0',port=5000)

