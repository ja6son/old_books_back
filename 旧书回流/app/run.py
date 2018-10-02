from flask import Flask,render_template,request,redirect,url_for,flash
import config
from exts import db
from models import User,Book,Comment


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

@app.route('/regist/',methods = ['POST','GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else :
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        passwords = request.form.get('passwords')
        if User.query.filter(User.user_name == user_name).first() :
            flash('该用户已存在')
            return redirect(url_for('regist'))
        elif password != passwords:
            flash('两次密码不同')
            return redirect(url_for('regist'))
        else :
            telephone = request.form.get('telephone')
            sex = request.form.get('sex')
            qq = request.form.get('qq')
            sign = request.form.get('sign')
            user = User(user_name = user_name,password = password,
                        telephone = telephone,qq = qq,sex = sex ,sign = sign)
            db.session.add(user)
            db.session.commit()
            return 'OK'

if __name__ == '__main__':
    app.run()