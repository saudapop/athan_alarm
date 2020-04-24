# from test import EVENTS, PREFERENCES
from actions import refresh_scheduling_program, get_preferences
from flask import Flask, request, render_template

app = Flask(__name__,
            static_url_path='',
            static_folder='client/dist',
            template_folder='client/dist')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-preferences/')
def preferences():
    return get_preferences()


@app.route('/api/update-scheduler/', methods=['POST'])
def update_and_restart_scheduler():
    NEW_PREFERENCES = request.get_json()
    refresh_scheduling_program(NEW_PREFERENCES)
    return '👍'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=86753)
