from flask import Flask
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

app = Flask(__name__)
CORS(app)
mysql = MySQL(app) 

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '725Donald725'
app.config['MYSQL_DATABASE_DB'] = 'facerecognition'
mysql.init_app(app)
