# API Usage

This document provides detailed information on how to use the API endpoints provided by the Smart Relay Control System.

## API Endpoints

### 1. Get Current Status

**Endpoint:** `GET /api/status`

**Description:** This endpoint retrieves the current status of the relay.

**Response:**

```json
{
  "status": "開啟" | "關閉"
}
```

### 2. Control Relay

**Endpoint:** `POST /api/control`

**Description:** This endpoint controls the relay by sending a command to turn it on or off.

**Request Body:**

```json
{
  "command": "on" | "off"
}
```

**Response:**

```json
{
  "status": "success" | "error",
  "message": "繼電器已開啟" | "繼電器已關閉" | "無效的命令",
  "timestamp": "YYYY-MM-DD HH:MM:SS" (if success)
}
```

### 3. Get Logs

**Endpoint:** `GET /api/logs`

**Description:** This endpoint retrieves the most recent action logs.

**Response:**

```json
{
  "logs": [
    {
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "status": "開啟" | "關閉"
    },
    ...
  ]
}
```

## Example Usage

### Get Current Status

```bash
curl -X GET http://<RaspberryPiIP>:5000/api/status
```

### Control Relay

#### Turn On

```bash
curl -X POST http://<RaspberryPiIP>:5000/api/control -H "Content-Type: application/json" -d '{"command": "on"}'
```

#### Turn Off

```bash
curl -X POST http://<RaspberryPiIP>:5000/api/control -H "Content-Type: application/json" -d '{"command": "off"}'
```

### Get Logs

```bash
curl -X GET http://<RaspberryPiIP>:5000/api/logs
```
