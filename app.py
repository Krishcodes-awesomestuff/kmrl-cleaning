from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

# --- Configuration ---
DATABASE_FILE = 'job_tracker.db'
API_PORT = 5000
# --------------------

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

@app.route('/')
def index():
    """Serves the main dashboard page."""
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def handle_tap():
    """Handles incoming RFID taps from the ESP8266."""
    data = request.get_json()
    uid = data.get('uid')
    if not uid:
        return jsonify({'status': 'error', 'message': 'Missing UID'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Find the employee associated with the UID
    cursor.execute("SELECT id, name FROM employees WHERE uid = ?", (uid,))
    employee = cursor.fetchone()

    if not employee:
        conn.close()
        return jsonify({'status': 'error', 'message': f'Unknown UID: {uid}'}), 404

    employee_id = employee['id']
    employee_name = employee['name']

    # 2. Check if there's an active job for this employee
    cursor.execute(
        "SELECT id FROM job_logs WHERE employee_id = ? AND status = 'In Progress'",
        (employee_id,)
    )
    active_job = cursor.fetchone()

    if active_job:
        # 3a. If a job is active, end it
        job_id = active_job['id']
        end_time = datetime.now()
        cursor.execute(
            "UPDATE job_logs SET end_time = ?, status = 'Completed' WHERE id = ?",
            (end_time, job_id)
        )
        message = f"Job completed for {employee_name}."
        print(f"✅ {message}")
    else:
        # 3b. If no job is active, start a new one
        start_time = datetime.now()
        cursor.execute(
            "INSERT INTO job_logs (employee_id, start_time, status) VALUES (?, ?, 'In Progress')",
            (employee_id, start_time)
        )
        message = f"Job started for {employee_name}."
        print(f"✅ {message}")

    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': message}), 200


@app.route('/status', methods=['GET'])
def get_status():
    """Provides data for the frontend dashboard."""
    conn = get_db_connection()
    
    # Get employees currently working
    in_progress_jobs = conn.execute('''
        SELECT e.name, j.start_time
        FROM job_logs j
        JOIN employees e ON j.employee_id = e.id
        WHERE j.status = 'In Progress'
        ORDER BY j.start_time DESC
    ''').fetchall()

    # Get the last 20 completed jobs
    completed_jobs = conn.execute('''
        SELECT e.name, j.start_time, j.end_time
        FROM job_logs j
        JOIN employees e ON j.employee_id = e.id
        WHERE j.status = 'Completed'
        ORDER BY j.end_time DESC
        LIMIT 20
    ''').fetchall()

    conn.close()

    return jsonify({
        'in_progress': [dict(job) for job in in_progress_jobs],
        'completed': [dict(job) for job in completed_jobs]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT, debug=True)