# PrepSpark 📚

A data-driven application to track study sessions, analyze productivity, and predict performance using Python, MySQL, and Streamlit.

## 🚀 Setup Instructions

### 1. Install Dependencies
Run the following command to install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 2. Database Setup
1.  Ensure you have **MySQL** installed and running.
2.  Create the database and table by executing the `schema.sql` file in your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or command line).
    ```sql
    SOURCE schema.sql;
    ```

### 3. Configure Connection
Open `db.py` and update the `password` field with your MySQL root password:
```python
password="your_actual_password"
```

### 4. Run the Application
Start the Streamlit app:
```bash
streamlit run app.py
```

## 📂 Project Structure
- `app.py`: Main application file.
- `db.py`: Database connection logic.
- `analytics.py`: Core logic for productivity, streaks, and burnout detection.
- `prediction.py`: Simple prediction model.
- `schema.sql`: Database schema.
