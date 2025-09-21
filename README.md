# KMRL Cleaning - Job Tracker System

A real-time job tracking system for KMRL cleaning staff using RFID technology and a web-based dashboard. This system allows employees to clock in/out using RFID cards and provides supervisors with real-time visibility into active jobs and completed work history.

## 🏗️ Project Structure

```
kmrl-cleaning/
├── app.py                 # Main Flask application
├── setup_database.py      # Database initialization script
├── job_tracker.db         # SQLite database (auto-generated)
├── instance/
│   └── cleaning_log.db    # Instance-specific database
└── templates/
    └── index.html         # Dashboard frontend
```

## ✨ Features

### 🎯 Core Functionality
- **RFID-based Clock In/Out**: Employees tap RFID cards to start/end jobs
- **Real-time Dashboard**: Live updates showing current workers and job history
- **Automatic Job Management**: System automatically starts new jobs or ends active ones
- **Employee Management**: Pre-configured employee database with RFID UIDs

### 📊 Dashboard Features
- **Active Workers Display**: Shows currently working employees with duration
- **Job Statistics**: Daily job counts, total hours, and active worker count
- **Recent Job History**: Last 20 completed jobs with duration calculations
- **Auto-refresh**: Dashboard updates every 10 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Professional UI**: Clean, modern interface with KMRL branding

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📋 Prerequisites

- Python 3.7+
- Flask
- SQLite3 (included with Python)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd kmrl-cleaning
```

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Initialize the Database
```bash
python setup_database.py
```

This will create:
- `job_tracker.db` with required tables
- Pre-configured employees with RFID UIDs

### 4. Start the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 👥 Employee Configuration

Default employees are configured in [`setup_database.py`](setup_database.py):

| Employee | RFID UID | 
|----------|----------|
| Mukesh | 53 65 4E 1C |
| Rakshana | 93 97 C1 2C |
| KP | CA 4C 65 7A |

### Adding New Employees

Edit the `EMPLOYEES` list in [`setup_database.py`](setup_database.py):

```python
EMPLOYEES = [
    ('53 65 4E 1C', 'Mukesh'),
    ('93 97 C1 2C', 'Rakshana'),
    ('CA 4C 65 7A', 'KP'),
    ('NEW_RFID_UID', 'New Employee Name')  # Add new employees here
]
```

Then run the setup script again:
```bash
python setup_database.py
```

## 🔌 API Endpoints

### POST `/data`
Handles RFID tap events from ESP8266 devices.

**Request Body:**
```json
{
    "uid": "53 65 4E 1C"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Job started for Mukesh."
}
```

### GET `/status`
Returns current system status for the dashboard.

**Response:**
```json
{
    "in_progress": [
        {
            "name": "Mukesh",
            "start_time": "2024-01-15T09:30:00"
        }
    ],
    "completed": [
        {
            "name": "Rakshana",
            "start_time": "2024-01-15T08:00:00",
            "end_time": "2024-01-15T12:00:00"
        }
    ]
}
```

### GET `/`
Serves the main dashboard interface.

## 🗄️ Database Schema

### `employees` Table
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
```

### `job_logs` Table
```sql
CREATE TABLE job_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    status TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);
```

## 📱 Hardware Integration

This system is designed to work with ESP8266 microcontrollers equipped with RFID readers. The ESP8266 should:

1. Read RFID card UIDs
2. Send POST requests to `/data` endpoint
3. Handle the JSON response for user feedback

### Sample ESP8266 Code Structure:
```cpp
// Read RFID UID
String uid = readRFID();

// Send to Flask API
HTTPClient http;
http.begin("http://your-server:5000/data");
http.addHeader("Content-Type", "application/json");
String payload = "{\"uid\":\"" + uid + "\"}";
int httpResponseCode = http.POST(payload);
```

## 🔧 Configuration

Key configuration options in [`app.py`](app.py):

```python
DATABASE_FILE = 'job_tracker.db'  # Database file path
API_PORT = 5000                   # Flask server port
```

## 🚦 System Workflow

1. **Employee arrives**: Taps RFID card on reader
2. **ESP8266**: Reads UID and sends to Flask API
3. **Flask API**: 
   - Looks up employee by UID
   - Checks for active jobs
   - Either starts new job or ends current job
4. **Dashboard**: Updates in real-time showing current status
5. **Employee leaves**: Taps card again to end job

## 📊 Dashboard Features

### Statistics Cards
- **Active Workers**: Count of employees currently working
- **Jobs Today**: Number of completed jobs today
- **Total Hours**: Sum of all work hours for the current day

### Active Workers Section
- Real-time list of employees currently working
- Shows start time and current duration
- Updates automatically every 10 seconds

### Job History Table
- Last 20 completed jobs
- Employee name, start/end times, and duration
- Sortable and responsive table design

## 🔄 Auto-refresh Behavior

The dashboard implements intelligent auto-refresh:
- Updates every 10 seconds when page is visible
- Pauses updates when page is hidden (browser tab inactive)
- Resumes updates when page becomes visible again
- Manual refresh button available

## 🎨 UI/UX Features

- **Responsive Design**: Works on all screen sizes
- **Professional Styling**: Clean, modern interface
- **Loading States**: Visual feedback during data fetching
- **Error Handling**: Graceful error display for network issues
- **Empty States**: Helpful messages when no data is available
- **Hover Effects**: Interactive elements with smooth transitions

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**: Run `python setup_database.py`
2. **Port already in use**: Change `API_PORT` in [`app.py`](app.py)
3. **RFID not recognized**: Check UID format in database
4. **Dashboard not loading**: Verify Flask server is running

### Debugging

Enable debug mode by ensuring this line in [`app.py`](app.py):
```python
app.run(host='0.0.0.0', port=API_PORT, debug=True)
```

## 📈 Future Enhancements

- Employee management interface
- Detailed reporting and analytics
- Export functionality (CSV/PDF)
- Email notifications for long shifts
- Multi-location support
- Role-based access control
- Mobile app for supervisors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for KMRL (Kochi Metro Rail Limited) internal use.

## 📞 Support

For technical support or questions, please contact the development team.
