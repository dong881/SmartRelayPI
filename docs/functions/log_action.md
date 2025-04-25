# `log_action` Function

The `log_action` function is responsible for recording the relay's action logs into the SQLite database. It logs the timestamp and status of each action performed on the relay.

## Function Definition

```python
def log_action(status):
    """記錄操作日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO relay_logs (timestamp, status) VALUES (?, ?)', 
                   (timestamp, status))
    conn.commit()
    conn.close()
    return timestamp
```

## Explanation

1. **Get Current Timestamp**: The function first gets the current timestamp using `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.

2. **Connect to Database**: The function then connects to the SQLite database specified by the `DB_PATH` variable using `sqlite3.connect(DB_PATH)`.

3. **Create Cursor**: A cursor object is created using `conn.cursor()` to execute SQL commands.

4. **Insert Log Entry**: The function executes an SQL command to insert a new log entry into the `relay_logs` table. The log entry includes the current timestamp and the status of the relay (e.g., "開啟" or "關閉").

5. **Commit and Close**: The function commits the changes to the database using `conn.commit()` and then closes the connection using `conn.close()`.

6. **Return Timestamp**: The function returns the timestamp of the log entry.

## Usage

The `log_action` function is typically called whenever an action is performed on the relay to record the action in the database.

```python
if command == 'on':
    # 開啟 - 低電平（繼電器通電）
    GPIO.output(RELAY_PIN, GPIO.LOW)
    timestamp = log_action("開啟")
    return jsonify({
        'status': 'success',
        'message': '繼電器已開啟',
        'timestamp': timestamp
    })
elif command == 'off':
    # 關閉 - 高電平（繼電器斷電）
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    timestamp = log_action("關閉")
    return jsonify({
        'status': 'success',
        'message': '繼電器已關閉',
        'timestamp': timestamp
    })
```

In this example, the `log_action` function is called after changing the relay's state to record the action in the database.
