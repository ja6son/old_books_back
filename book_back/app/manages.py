from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from app import app
from exts import db
from models import User,Book

manage = Manager(app)

migrate = Migrate(app,db)

manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()