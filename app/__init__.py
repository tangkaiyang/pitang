from flask import Flask
from config import Config

pitang = Flask(__name__)


pitang.config.from_object(Config)
