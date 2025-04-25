# `index` Function

The `index` function is responsible for rendering the main page of the web application. It retrieves the current status of the relay and passes it to the HTML template for display.

## Function Definition

```python
@app.route('/')
def index():
    """渲染主頁"""
    return render_template('index.html', status=get_current_status())
```

## Explanation

1. **Route Definition**: The function is decorated with `@app.route('/')`, which means it will handle requests to the root URL (`/`) of the web application.

2. **Render Template**: The function calls `render_template('index.html', status=get_current_status())` to render the `index.html` template. It passes the current status of the relay (obtained by calling `get_current_status()`) as a variable named `status` to the template.

## Usage

The `index` function is automatically called when a user accesses the root URL of the web application. It renders the main page with the current status of the relay.

```python
if __name__ == '__main__':
    try:
        init_db()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()  # 確保程序結束時清理 GPIO
```

In this example, the `index` function is part of the Flask application and is called when the application is running and a user accesses the root URL.
