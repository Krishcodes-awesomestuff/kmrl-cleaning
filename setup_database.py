import sqlite3

# --- Configuration ---
DATABASE_FILE = 'job_tracker.db'
EMPLOYEES = [
    ('53 65 4E 1C', 'Mukesh'),
    ('93 97 C1 2C', 'Rakshana'),
    ('CA 4C 65 7A', 'KP')
    # Add more employees here as needed
]
# --------------------

def setup():
    """Creates the database tables and populates the employees."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        )
    ''')
    print("Employees table created or already exists.")

    # Create job_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees (id)
        )
    ''')
    print("Job logs table created or already exists.")

    # Add employees, ignoring duplicates
    for uid, name in EMPLOYEES:
        try:
            cursor.execute("INSERT INTO employees (uid, name) VALUES (?, ?)", (uid, name))
            print(f"Added employee: {name} with UID: {uid}")
        except sqlite3.IntegrityError:
            print(f"Employee {name} with UID {uid} already exists.")

    conn.commit()
    conn.close()
    print("\nDatabase setup complete!")

if __name__ == '__main__':
    setup()