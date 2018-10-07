from flask import Flask,render_template,request,redirect,url_for,flash,session
import config
from exts import db
from models import User,Book,Comment


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/login/',methods = ['POST','GET'])  
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else :
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter(User.user_name == user_name).first()
        if user:
            if user.password == password :
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else :
                flash('密码错误')
                return redirect(url_for('login'))
        else :
            flash('无此用户')
            return redirect(url_for('login'))


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
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id :
        user = User.query.filter(User.id == user_id).first()
        return {'user':user}
    else :
        return {}



if __name__ == '__main__':
    app.run()