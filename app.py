from flask import Flask, render_template, url_for, request, flash
import model


flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'aboba1488'


@flask_app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
