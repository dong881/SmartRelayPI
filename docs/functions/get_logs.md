# `get_logs` Function

The `get_logs` function is responsible for retrieving the most recent action logs from the SQLite database. It returns a list of log entries, each containing a timestamp and status.

## Function Definition

```python
def get_logs(limit=100):
    """獲取最近的操作日誌"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, status FROM relay_logs ORDER BY id DESC LIMIT ?', 
                   (limit,))
    logs = [{'timestamp': row[0], 'status': row[1]} for row in cursor.fetchall()]
    conn.close()
    return logs
```

## Explanation

1. **Connect to Database**: The function connects to the SQLite database specified by the `DB_PATH` variable using `sqlite3.connect(DB_PATH)`.

2. **Create Cursor**: A cursor object is created using `conn.cursor()` to execute SQL commands.

3. **Retrieve Logs**: The function executes an SQL command to select the `timestamp` and `status` columns from the `relay_logs` table, ordered by `id` in descending order, and limited to the specified number of entries (default is 100).

4. **Fetch and Format Logs**: The function fetches the results of the query using `cursor.fetchall()` and formats them into a list of dictionaries, where each dictionary represents a log entry with `timestamp` and `status` keys.

5. **Close Connection**: The function closes the database connection using `conn.close()`.

6. **Return Logs**: The function returns the list of log entries.

## Usage

The `get_logs` function is typically called to retrieve the most recent action logs for display or analysis.

```python
@app.route('/api/logs')
def logs():
    """獲取操作日誌 API"""
    return jsonify({
        'logs': get_logs()
    })
```

In this example, the `get_logs` function is used in an API endpoint to return the most recent action logs as a JSON response.
