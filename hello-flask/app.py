from flask import Flask, render_template
from ledcontroller import LEDController
import datetime


app = Flask(__name__)


@app.route('/')
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString,
        'message': 'this is a message',
        'content': 'this is some content',
    }
    return render_template('index.html', **templateData)

@app.route('/led')
def led():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString,
        'message': 'this is a message',
        'content': 'this is some content',
    }


    led_controller = LEDController()
    return render_template('index.html', **templateData)


@app.route('/api/data')
def get_data():
    return app.send_static_file('data.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)