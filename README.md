# 樹莓派智慧繼電器控制系統

這是一個基於 Flask 和 Docker 的樹莓派智慧繼電器控制系統。系統提供了一個簡潔的 Web 界面，用於控制 GPIO 腳位，同時記錄操作歷史。

## 功能特點

- 簡潔質感風格的網頁界面
- 滑動開關控制繼電器狀態（開/關）
- 關閉操作時使用 SweetAlert2 進行二次確認
- 顯示最近 100 筆操作記錄（包含時間戳）
- Docker 容器化部署
- 使用 GPIO2 控制繼電器
- 適用於常閉型繼電器

## 安裝與部署

### 前提條件

- 樹莓派（任何型號）
- 已安裝 Docker 和 Docker Compose
- 已連接繼電器模組到 GPIO2

### 安裝 Docker 和 Docker Compose

在樹莓派上安裝 Docker 和 Docker Compose，請依照以下步驟進行：

#### 安裝 Docker

1. 更新系統套件：

```bash
sudo apt update
sudo apt upgrade -y
```

2. 安裝必要的依賴：

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

3. 下載並安裝 Docker 的便捷腳本：

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

4. 將當前用戶添加到 docker 用戶組以避免每次都需要 sudo：

```bash
sudo usermod -aG docker $USER
```

5. 啟用 Docker 服務：

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

6. 登出並重新登入或重啟系統以應用用戶組更改：

```bash
sudo reboot
```

#### 安裝 Docker Compose

1. 下載並安裝 Docker Compose：

```bash
sudo apt install -y python3-pip
sudo pip3 install docker-compose
```

2. 驗證安裝：

```bash
docker --version
docker-compose --version
```

如果命令顯示版本號碼，則表示安裝成功。

### 一鍵部署

1. 克隆本倉庫：

```bash
git clone https://github.com/yourusername/raspberry-pi-relay-control.git
cd SmartRelayPI
```

2. 啟動服務：

```bash
docker-compose up -d
```

3. 訪問界面：

打開瀏覽器，訪問 `http://樹莓派IP:5000`

## 繼電器連接

- 繼電器控制腳連接到 GPIO2
- 系統設計為適用於常閉型繼電器
- 高電平（GPIO.HIGH）= 關閉（繼電器斷電）
- 低電平（GPIO.LOW）= 開啟（繼電器通電）

## API 接口

- `GET /api/status` - 獲取當前繼電器狀態
- `POST /api/control` - 控制繼電器，請求體 `{"command": "on|off"}`
- `GET /api/logs` - 獲取操作歷史記錄

## 文件結構

```
.
├── Dockerfile
├── docker-compose.yml
├── app.py                # 主應用程式
├── requirements.txt      # Python 依賴
├── data/                 # 資料存儲目錄
│   └── relay_logs.db     # SQLite 資料庫
├── static/               # 靜態資源
│   ├── style.css         # CSS 樣式
│   └── script.js         # JavaScript 腳本
└── templates/            # HTML 模板
    └── index.html        # 主頁面
```

## 注意事項

- 確保 Docker 容器以特權模式運行（已在 docker-compose.yml 中設置）
- 如果需要更改 GPIO 腳位，請修改 `app.py` 中的 `RELAY_PIN` 變量
- 系統會在容器啟動時自動創建數據庫
- 如果遇到權限問題，可能需要使用 `sudo` 運行 Docker 相關命令

# Raspberry Pi Smart Relay Control System

This is a Raspberry Pi smart relay control system based on Flask and Docker. The system provides a simple web interface for controlling GPIO pins and recording operation history.

## Features

- Simple and elegant web interface
- Toggle switch to control relay state (on/off)
- SweetAlert2 confirmation for off operations
- Display the last 100 operation logs (with timestamps)
- Docker containerized deployment
- Use GPIO2 to control the relay
- Suitable for normally closed relays

## Installation and Deployment

### Prerequisites

- Raspberry Pi (any model)
- Docker and Docker Compose installed
- Relay module connected to GPIO2

### Install Docker and Docker Compose

To install Docker and Docker Compose on Raspberry Pi, follow these steps:

#### Install Docker

1. Update system packages:

```bash
sudo apt update
sudo apt upgrade -y
```

2. Install necessary dependencies:

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

3. Download and install Docker's convenience script:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

4. Add the current user to the docker group to avoid needing sudo every time:

```bash
sudo usermod -aG docker $USER
```

5. Enable Docker service:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

6. Log out and log back in or reboot the system to apply the group changes:

```bash
sudo reboot
```

#### Install Docker Compose

1. Download and install Docker Compose:

```bash
sudo apt install -y python3-pip
sudo pip3 install docker-compose
```

2. Verify the installation:

```bash
docker --version
docker-compose --version
```

If the commands show version numbers, the installation was successful.

### One-click Deployment

1. Clone this repository:

```bash
git clone https://github.com/yourusername/raspberry-pi-relay-control.git
cd SmartRelayPI
```

2. Start the service:

```bash
docker-compose up -d
```

3. Access the interface:

Open a browser and visit `http://RaspberryPiIP:5000`

## Relay Connection

- Relay control pin connected to GPIO2
- System designed for normally closed relays
- High level (GPIO.HIGH) = Off (relay de-energized)
- Low level (GPIO.LOW) = On (relay energized)

## API Endpoints

- `GET /api/status` - Get the current relay status
- `POST /api/control` - Control the relay, request body `{"command": "on|off"}`
- `GET /api/logs` - Get operation history logs

## File Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── app.py                # Main application
├── requirements.txt      # Python dependencies
├── data/                 # Data storage directory
│   └── relay_logs.db     # SQLite database
├── static/               # Static resources
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript scripts
└── templates/            # HTML templates
    └── index.html        # Main page
```

## Notes

- Ensure the Docker container runs in privileged mode (set in docker-compose.yml)
- If you need to change the GPIO pin, modify the `RELAY_PIN` variable in `app.py`
- The system will automatically create the database when the container starts
- If you encounter permission issues, you may need to run Docker-related commands with `sudo`

## Documentation

- [Chinese Documentation](docs/README_zh.md)
- [English Documentation](docs/README_en.md)
- [API Usage](docs/api_usage.md)
- [Function Documentation](docs/functions/)

### Function Documentation

- [init_db](docs/functions/init_db.md)
- [log_action](docs/functions/log_action.md)
- [get_logs](docs/functions/get_logs.md)
- [get_current_status](docs/functions/get_current_status.md)
- [index](docs/functions/index.md)
- [status](docs/functions/status.md)
- [control](docs/functions/control.md)
- [logs](docs/functions/logs.md)
