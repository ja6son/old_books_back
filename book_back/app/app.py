import config,os
from flask import Flask,render_template,request,redirect,url_for,flash,session
from exts import db
from models import User,Book
from decorators import login_judge


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

#登录
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

#注册
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
            if telephone and sex and qq and sign :
                user = User(user_name= user_name, password=password,
                            telephone=telephone, qq=qq, sex=sex, sign=sign)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else :
                flash('请将信息填写完整')
                return redirect(url_for('regist'))

#注销
@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

#发布新书
@app.route('/book/',methods = ['POST','GET'])
@login_judge
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
            book = Book(book_name=book_name,book_type=book_type, 
                            fee=fee,content=content)  #生成新对象
            book_image = user.user_name + '_' + book_name + '.jpg' #图书照片图片
            book.book_image = book_image
            UPLOAD_FOLDER = r'C:\mygit\book_back\app\static\images'
            book_img.save(os.path.join( UPLOAD_FOLDER , book_image)) 
            book.user = user
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('index'))
        else :
            flash('填写不完整，请重新填写')
            return redirect(url_for('book'))

#个人中心
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
        avatar = request.files.get('avatar')
        ava_name = 'ava_' + user.user_name + str(user.avatar_id) + '.jpg'
        user.avatar = ava_name
        user.avatar_id = user.avatar_id + 1
        UPLOAD_FOLDER = r'C:\mygit\book_back\app\static\images'
        avatar.save(os.path.join( UPLOAD_FOLDER , ava_name)) 
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('my_center'))

#修改密码
@app.route('/password', methods = ['GET', 'POST'])
def password():
    if request.method == 'GET':
        return render_template('password.html')
    else :
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        old_pass = request.form.get('old_pass')
        if old_pass == user.password:
            new_pass = request.form.get('new_pass')
            new_pass2 = request.form.get('new_pass2')
            if new_pass == new_pass2:
                user.password = new_pass
                db.session.commit()
                flash('修改成功')
                return redirect(url_for('password'))
            else :
                flash('两次新密码不同')
                return redirect(url_for('password'))
        else:
            flash('密码错误')
            return redirect(url_for('password'))

@app.route('/category/<name>/<page>')
def category(name,page):
    page = request.args.get('page', 1)
    per_page = 8
    pagination = Book.query.filter(Book.book_type == name).paginate(page, per_page = per_page)
    books = pagination.items
    return render_template('cate.html', books = books, pagination = pagination ,book_name = name)

#书的详情
@app.route('/detail/<book_id>')
def detail(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    return render_template('detail.html', book=book)

#管理书籍
@app.route('/manage')
@login_judge
def manage():
    user_id = session.get('user_id')
    books = Book.query.filter(Book.user_id == user_id).all()
    return render_template('manage.html', books = books)

#删除书籍
@app.route('/delete/<book_id>')
def delete(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('manage'))

#编辑书籍
@app.route('/edit/<book_id>',methods = ['GET', 'POST'])
def edit(book_id):
    if request.method == 'GET':
        book = Book.query.filter(Book.id == book_id).first()
        return render_template('edit.html', book = book)
    else :
        book_name = request.form.get('book_name')
        book_type = request.form.get('book_type')
        fee = request.form.get('fee')
        content = request.form.get('content')
        if book_name and fee and content and book_type:
            user_id = session.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            book = Book.query.filter(Book.id == book_id).first()
            book.book_name = book_name
            book.book_type = book_type
            book.fee = fee
            book.content = content
            db.session.commit()
            flash('修改成功')
            return redirect(url_for('edit', book_id=book_id))
        else :
            flash('填写不完整，请重新填写')
            return redirect(url_for('edit', book_id=book_id))

#搜索
@app.route('/search', methods = ['POST'])
def search():
    sear = request.form.get('sear')
    return redirect(url_for('content', sear=sear))
#搜索内容

@app.route('/content/<sear>')
def content(sear):
    books = Book.query.filter(Book.book_name.like( '%{}%'.format(sear) ))
    return render_template('content.html', books=books)

#传入用户对象
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