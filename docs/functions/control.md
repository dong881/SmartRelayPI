# `control` Function

The `control` function is responsible for handling the API endpoint that controls the relay. It processes the incoming command to turn the relay on or off and logs the action.

## Function Definition

```python
@app.route('/api/control', methods=['POST'])
def control():
    """控制繼電器 API"""
    data = request.get_json()
    command = data.get('command')
    
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
    else:
        return jsonify({
            'status': 'error',
            'message': '無效的命令'
        }), 400
```

## Explanation

1. **Route Definition**: The function is defined as a route for the `/api/control` endpoint with the `POST` method using the `@app.route` decorator.

2. **Get JSON Data**: The function retrieves the JSON data from the incoming request using `request.get_json()`.

3. **Extract Command**: The function extracts the `command` value from the JSON data.

4. **Process Command**: The function checks the value of the `command`:
   - If the command is `'on'`, it sets the GPIO output to `LOW` to turn on the relay, logs the action with the status "開啟", and returns a success response with a message and timestamp.
   - If the command is `'off'`, it sets the GPIO output to `HIGH` to turn off the relay, logs the action with the status "關閉", and returns a success response with a message and timestamp.
   - If the command is invalid, it returns an error response with a status code of 400.

## Usage

The `control` function is used to handle API requests for controlling the relay. It processes the incoming command to turn the relay on or off and logs the action.

```python
@app.route('/api/control', methods=['POST'])
def control():
    """控制繼電器 API"""
    data = request.get_json()
    command = data.get('command')
    
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
    else:
        return jsonify({
            'status': 'error',
            'message': '無效的命令'
        }), 400
```

In this example, the `control` function is used to handle API requests for controlling the relay. It processes the incoming command to turn the relay on or off and logs the action.
