from flask import Flask
from DataCollectorMicroservice import app

appl = Flask(__name__)
appl.register_blueprint(app)

appl.run(port=5005)