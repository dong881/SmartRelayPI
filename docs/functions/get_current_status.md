# `get_current_status` Function

The `get_current_status` function is responsible for retrieving the current state of the relay. It reads the GPIO pin state and returns a string indicating whether the relay is "開啟" (on) or "關閉" (off).

## Function Definition

```python
def get_current_status():
    """獲取當前狀態"""
    # 讀取 GPIO 狀態
    state = GPIO.input(RELAY_PIN)
    return "關閉" if state == GPIO.HIGH else "開啟"
```

## Explanation

1. **Read GPIO State**: The function reads the state of the GPIO pin connected to the relay using `GPIO.input(RELAY_PIN)`. The `RELAY_PIN` variable specifies the GPIO pin number.

2. **Determine Relay State**: The function checks the state of the GPIO pin:
   - If the state is `GPIO.HIGH`, it means the relay is off, and the function returns the string "關閉".
   - If the state is not `GPIO.HIGH`, it means the relay is on, and the function returns the string "開啟".

## Usage

The `get_current_status` function is typically called to retrieve the current state of the relay, either for display purposes or for API responses.

```python
@app.route('/api/status')
def status():
    """獲取當前狀態 API"""
    return jsonify({
        'status': get_current_status()
    })
```

In this example, the `get_current_status` function is used in the `/api/status` route to provide the current relay state as a JSON response.
