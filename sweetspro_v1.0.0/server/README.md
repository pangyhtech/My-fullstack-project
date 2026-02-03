# SweetsPro Backend Server

Simple HTTP server for the SweetsPro iOS application.

---

## Quick Start
```bash
cd sweetspro_v1.0.0/server
python3 server.py
```

Server runs at: **http://localhost:8080**

## API Endpoints
- Products: `GET /api/products`
- Images: `GET /images/{image_name}.png`

## Tech
- Python 3.x
- HTTPServer
- In-memory storage

## iOS Integration
- **Simulator:** Use `localhost:8080`
- **Physical Device:** Replace with Mac's IP address
