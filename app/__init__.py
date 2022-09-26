from flask import Flask
from flask_cors import CORS
from config import Config

pitang = Flask(__name__)
CORS(pitang, supports_credentials=True)

pitang.config.from_object(Config)
