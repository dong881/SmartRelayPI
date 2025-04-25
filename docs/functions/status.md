# `status` Function

The `status` function is an API endpoint in the Flask application that retrieves the current status of the relay. It returns the status as a JSON response.

## Function Definition

```python
@app.route('/api/status')
def status():
    """獲取當前狀態 API"""
    return jsonify({
        'status': get_current_status()
    })
```

## Explanation

- **Route**: The function is mapped to the `/api/status` route using the `@app.route` decorator.
- **Method**: The function uses the `GET` method to retrieve the current status.
- **Response**: The function returns a JSON response containing the current status of the relay. The status is obtained by calling the `get_current_status` function.

## Usage

To use this API endpoint, send a `GET` request to `/api/status`. The response will be a JSON object containing the current status of the relay.

### Example Request

```bash
curl -X GET http://<RaspberryPiIP>:5000/api/status
```

### Example Response

```json
{
    "status": "開啟"
}
```

In this example, the response indicates that the relay is currently "開啟" (on).
