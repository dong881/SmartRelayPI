# `logs` Function

The `logs` function is responsible for handling the API endpoint that retrieves the most recent action logs from the SQLite database. It returns a JSON response containing a list of log entries, each with a timestamp and status.

## Function Definition

```python
@app.route('/api/logs')
def logs():
    """獲取操作日誌 API"""
    return jsonify({
        'logs': get_logs()
    })
```

## Explanation

1. **Route Definition**: The function is decorated with `@app.route('/api/logs')`, which defines the URL endpoint for the API. When a GET request is made to this endpoint, the `logs` function is called.

2. **Return JSON Response**: The function returns a JSON response using `jsonify()`. The response contains a single key, `logs`, which holds the result of the `get_logs()` function.

3. **Get Logs**: The `get_logs()` function is called to retrieve the most recent action logs from the SQLite database. The logs are returned as a list of dictionaries, each containing a `timestamp` and `status`.

## Usage

The `logs` function is typically called when a client (e.g., a web browser or a mobile app) makes a GET request to the `/api/logs` endpoint to retrieve the most recent action logs.

```python
@app.route('/api/logs')
def logs():
    """獲取操作日誌 API"""
    return jsonify({
        'logs': get_logs()
    })
```

In this example, the `logs` function is used to handle the API request and return the most recent action logs as a JSON response.
