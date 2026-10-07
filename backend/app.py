"""Research Opportunity Portal - P24-0631, BCS-5C."""
import os
from pathlib import Path
from datetime import date, datetime
from contextlib import contextmanager
import pymysql
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')
app = Flask(__name__, static_folder=str(ROOT / 'frontend'), static_url_path='/assets')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024
TEXT_FIELDS = {'title': 200, 'description': 10000, 'research_area': 100,
               'faculty_name': 100, 'department': 100, 'required_skills': 1000}
FIELDS = [*TEXT_FIELDS, 'available_positions', 'application_deadline', 'status']

@contextmanager
def database():
    connection = pymysql.connect(host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'research_portal'),
        password=os.getenv('DB_PASSWORD', ''), database=os.getenv('DB_NAME', 'research_portal'),
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=5)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def serialize(row):
    return {key: value.isoformat() if isinstance(value, (date, datetime)) else value
            for key, value in row.items()}

def validate(data):
    if not isinstance(data, dict):
        return None, {'body': 'Send a JSON object.'}
    errors, cleaned = {}, {}
    unknown = set(data) - set(FIELDS)
    if unknown:
        errors['body'] = 'Unknown fields: ' + ', '.join(sorted(unknown))
    for field, limit in TEXT_FIELDS.items():
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors[field] = 'This field is required and must be text.'
        elif len(value.strip()) > limit:
            errors[field] = f'Maximum length is {limit} characters.'
        else:
            cleaned[field] = value.strip()
    positions = data.get('available_positions')
    if type(positions) is not int or not 1 <= positions <= 10000:
        errors['available_positions'] = 'Enter an integer between 1 and 10000.'
    else:
        cleaned['available_positions'] = positions
    deadline = data.get('application_deadline')
    try:
        if not isinstance(deadline, str) or len(deadline) != 10:
            raise ValueError()
        parsed = date.fromisoformat(deadline).isoformat()
        if parsed != deadline:
            raise ValueError()
        cleaned['application_deadline'] = parsed
    except ValueError:
        errors['application_deadline'] = 'Enter a valid date in YYYY-MM-DD format.'
    status = data.get('status', 'Open')
    if status not in ('Open', 'Closed'):
        errors['status'] = 'Status must be Open or Closed.'
    else:
        cleaned['status'] = status
    return cleaned, errors

@app.get('/')
def home():
    return send_from_directory(ROOT / 'frontend', 'index.html')

@app.get('/api/health')
def health():
    with database() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return jsonify(status='ok', database='MySQL')

@app.route('/api/opportunities', methods=['GET', 'POST'])
def opportunities():
    if request.method == 'GET':
        with database() as connection, connection.cursor() as cursor:
            cursor.execute('SELECT * FROM opportunities ORDER BY id DESC')
            rows = cursor.fetchall()
        return jsonify(data=[serialize(row) for row in rows]), 200
    data, errors = validate(request.get_json(silent=True))
    if errors:
        return jsonify(message='Validation failed.', errors=errors), 400
    with database() as connection, connection.cursor() as cursor:
        cursor.execute('INSERT INTO opportunities (' + ','.join(FIELDS) + ') VALUES ('
                       + ','.join(['%s'] * len(FIELDS)) + ')', [data[field] for field in FIELDS])
        opportunity_id = cursor.lastrowid
        cursor.execute('SELECT * FROM opportunities WHERE id=%s', (opportunity_id,))
        row = cursor.fetchone()
    response = jsonify(message='Opportunity created.', data=serialize(row))
    response.headers['Location'] = f'/api/opportunities/{opportunity_id}'
    return response, 201

@app.route('/api/opportunities/<int:opportunity_id>', methods=['GET', 'PUT', 'DELETE'])
def opportunity(opportunity_id):
    with database() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM opportunities WHERE id=%s', (opportunity_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify(message='Research opportunity not found.'), 404
        if request.method == 'GET':
            return jsonify(data=serialize(row)), 200
        if request.method == 'DELETE':
            cursor.execute('DELETE FROM opportunities WHERE id=%s', (opportunity_id,))
            return jsonify(message='Opportunity deleted.', id=opportunity_id), 200
        incoming = request.get_json(silent=True)
        if not isinstance(incoming, dict) or not incoming:
            return jsonify(message='Validation failed.', errors={'body': 'Send a non-empty JSON object.'}), 400
        # Accept full or partial updates, including a status-only update.
        merged = {field: serialize(row)[field] for field in FIELDS}
        merged.update(incoming)
        data, errors = validate(merged)
        if errors:
            return jsonify(message='Validation failed.', errors=errors), 400
        cursor.execute('UPDATE opportunities SET ' + ','.join(field + '=%s' for field in FIELDS)
                       + ' WHERE id=%s', [data[field] for field in FIELDS] + [opportunity_id])
        cursor.execute('SELECT * FROM opportunities WHERE id=%s', (opportunity_id,))
        updated = cursor.fetchone()
    return jsonify(message='Opportunity updated.', data=serialize(updated)), 200

@app.errorhandler(HTTPException)
def http_error(error):
    return jsonify(message=error.description), error.code

@app.errorhandler(Exception)
def server_error(error):
    app.logger.exception('Request failed')
    return jsonify(message='Internal server error. Check the server log and database connection.'), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.getenv('PORT', '5000')), debug=False)

