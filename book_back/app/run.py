from flask import Flask,render_template,request,redirect,url_for,flash,session
import config,os
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
            user = User(user_name,password,
                        telephone,qq,sex ,sign)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/book/',methods = ['POST','GET'])
def book():
    if request.method == 'GET':
        return render_template('book.html')
    else:
        book_name = request.form.get('book_name')
        book_type = request.form.get('book_type')
        fee = request.form.get('fee')
        content = request.form.get('content')
        book_img = request.files.get('book_img')
        if book_name and fee and content and book_img and book_type:
            user_id = session.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            book = Book(book_name,book_type,fee,content)
            book_image = user.user_name + '_' + book_name + '.jpg'
            book.book_image = book_image
            UPLOAD_FOLDER = r'C:\mygit\旧书回流\app\static\images'
            book_img.save(os.path.join( UPLOAD_FOLDER , book_image))
            book.user = user
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('index'))
        else :
            flash('填写不完整，请重新填写')
            return redirect(url_for('book'))

@app.route('/my_center/',methods = ['GET','POST'])
def my_center():
    if request.method == 'GET':
        return render_template('my_center.html')
    else :
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.user_name = request.form.get('user_name')
        user.telephone = request.form.get('telephone')
        user.qq = request.form.get('qq')
        user.sex = request.form.get('sex')
        user.sign = request.form.get('sign')
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('my_center'))

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