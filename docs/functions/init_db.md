# `init_db` Function

The `init_db` function is responsible for initializing the SQLite database used to store relay logs. It ensures that the necessary database file and table are created if they do not already exist.

## Function Definition

```python
def init_db():
    """初始化數據庫"""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relay_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()
```

## Explanation

1. **Create Data Directory**: The function first ensures that the `data` directory exists. If it does not, it creates the directory using `os.makedirs('data', exist_ok=True)`.

2. **Connect to Database**: The function then connects to the SQLite database specified by the `DB_PATH` variable using `sqlite3.connect(DB_PATH)`.

3. **Create Cursor**: A cursor object is created using `conn.cursor()` to execute SQL commands.

4. **Create Table**: The function executes an SQL command to create the `relay_logs` table if it does not already exist. The table has three columns:
   - `id`: An integer primary key that auto-increments.
   - `timestamp`: A text field to store the timestamp of the log entry.
   - `status`: A text field to store the status of the relay (e.g., "開啟" or "關閉").

5. **Commit and Close**: The function commits the changes to the database using `conn.commit()` and then closes the connection using `conn.close()`.

## Usage

The `init_db` function is typically called at the start of the application to ensure that the database is properly set up before any operations are performed.

```python
if __name__ == '__main__':
    try:
        init_db()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()  # 確保程序結束時清理 GPIO
```

In this example, the `init_db` function is called before starting the Flask application to ensure that the database is initialized.
