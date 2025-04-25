#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time
import os
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# GPIO 設置
RELAY_PIN = 2  # 繼電器控制腳位設定為 GPIO2
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # 初始狀態為高電平（繼電器常閉）

# 資料庫設置
DB_PATH = 'data/relay_logs.db'

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

def get_logs(limit=100):
    """獲取最近的操作日誌"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, status FROM relay_logs ORDER BY id DESC LIMIT ?', 
                   (limit,))
    logs = [{'timestamp': row[0], 'status': row[1]} for row in cursor.fetchall()]
    conn.close()
    return logs

def get_current_status():
    """獲取當前狀態"""
    # 讀取 GPIO 狀態
    state = GPIO.input(RELAY_PIN)
    return "關閉" if state == GPIO.HIGH else "開啟"

@app.route('/')
def index():
    """渲染主頁"""
    return render_template('index.html', status=get_current_status())

@app.route('/api/status')
def status():
    """獲取當前狀態 API"""
    return jsonify({
        'status': get_current_status()
    })

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

@app.route('/api/logs')
def logs():
    """獲取操作日誌 API"""
    return jsonify({
        'logs': get_logs()
    })

if __name__ == '__main__':
    try:
        init_db()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()  # 確保程序結束時清理 GPIO