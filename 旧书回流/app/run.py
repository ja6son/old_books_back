from flask import Flask,render_template,request
import config
from exts import db


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('base.html')

@app.route('/login/',methods = ['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else :
        pass

if __name__ == '__main__':
    app.run()