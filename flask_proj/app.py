from flask import Flask
from flask_restful import Api
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.db'
api = Api(app)

login_manager = LoginManager(app)
SECRET_KEY = '43259M86MTV72POWITUVWSOLEIRVMU'
app.config['SECRET_KEY'] = SECRET_KEY


from flask_proj import *
if __name__ == '__main__':
    app.run(debug=True,port=8080)