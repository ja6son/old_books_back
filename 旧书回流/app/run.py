from flask import Flask,render_template
import config

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    app.run()