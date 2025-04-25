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
