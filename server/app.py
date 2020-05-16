from flask import Flask, request, render_template, jsonify
from utils.actions import refresh_scheduling_program, get_preferences
from utils.preferences_validation import validate_preferences_payload, UpdatePreferencesException

app = Flask(__name__,
            static_url_path='',
            static_folder='../client/dist',
            template_folder='../client/dist')


@app.errorhandler(UpdatePreferencesException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-preferences/')
def preferences():
    return jsonify(get_preferences())


@app.route('/api/update-scheduler/', methods=['POST'])
def update_and_restart_scheduler():
    NEW_PREFERENCES = request.get_json()
    validate_preferences_payload(NEW_PREFERENCES)
    refresh_scheduling_program(NEW_PREFERENCES)
    return '👍 its good!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
