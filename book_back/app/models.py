from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    user_name = db.Column(db.String(30),nullable = False)
    password = db.Column(db.String(50),nullable = False)
    telephone = db.Column(db.String(20),nullable = False)
    qq = db.Column(db.String(20),nullable = False)
    sex = db.Column(db.String(10),nullable = False)
    sign = db.Column(db.String(100),nullable = False)
    avatar = db.Column(db.String(128),default = "default_avatar.jpg")
    avatar_id = db.Column(db.Integer,default = 1)
    books = db.relationship('Book',backref = 'user')
    comments = db.relationship('Comment',backref = 'user')

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    book_name = db.Column(db.String(50),nullable = False)
    book_type =db.Column(db.String(10),nullable = False)
    fee = db.Column(db.String(20),default = '0.00')
    content = db.Column(db.Text,nullable = False)
    book_image = db.Column(db.String(128),default = "default_book_image.jpg")
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comments = db.relationship('Comment',backref = 'book')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    content = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'))
