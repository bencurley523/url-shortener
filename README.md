# High-Performance Async URL Shortener

A high-concurrency URL shortener built for speed. It uses an **asynchronous** architecture to handle high traffic loads, implements **Redis caching** for sub-millisecond read times, and is fully containerized with **Docker**.

## 🚀 Tech Stack

* **Backend:** Python 3.12+, FastAPI, Uvicorn, Motor (Async MongoDB Driver)
* **Database:** MongoDB (Local Docker container or Atlas Cloud)
* **Caching:** Redis (Cache-Aside pattern)
* **Infrastructure:** Docker & Docker Compose
* **Tooling:** `uv` (Fast Python package manager)

## ✨ Features

* **⚡ High Performance:** Capable of handling ~1k+ RPS (Requests Per Second) via Redis caching.
* **🔄 Async Architecture:** Non-blocking I/O for database operations and request handling.
* **🐳 Fully Containerized:** One command (`docker compose up`) sets up the API, MongoDB, and Redis.
* **📊 Analytics:** Tracks click counts and timestamps asynchronously (Fire-and-forget). # TODO
* **🔗 Core Features:** Shortening, Custom Aliases, Redirection (HTTP 307), and Duplicate Prevention.

## 📂 Project Structure

```text
url-shortener/
├── backend/                # Backend Application Code
│   ├── __init__.py
│   ├── crud.py             # Database & Cache operations (Create, Read, Update)
│   ├── database.py         # DB Configuration & Connection setup
│   ├── main.py             # FastAPI Routes & Controller
│   ├── models.py           # Pydantic Data Models
│   ├── utils.py            # Helper functions (Base62 encoding)
├── frontend/               # User Interface
│   ├── index.html
│   ├── script.js
│   ├── styles.css
├── .env                    # Environment Variables (Excluded from Git)
├── .dockerignore           # Docker exclusion rules
├── benchmark.py            # Load testing script
├── compose.yaml            # Docker Compose orchestration
├── Dockerfile              # Backend container definition
├── pyproject.toml          # Dependencies (uv)
├── README.md               # Documentation
├── requirements.txt        # Frozen dependencies for Docker
└── uv.lock                 # Dependency lockfile
```

## 🛠️ Setup & Installation

You can run this project in two ways: **Docker (Recommended)** or **Manual Local Dev**.

### Method 1: Docker (Fastest)
This sets up the API, MongoDB, and Redis automatically.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/bencurley523/url-shortener.git
    cd url-shortener
    ```

2.  **Configuration (.env)**
    Create a `.env` file in the root. Docker will read these values.
    ```env
    MONGO_URI=mongodb://mongo:27017
    DB_NAME=shortener_db
    REDIS_URL=redis://redis:6379
    CACHE_TTL=3600
    ```

3.  **Run with Docker Compose**
    ```bash
    docker compose up -d --build
    ```
    *The backend API will be available at `http://localhost:8000`.*

---

### Method 2: Manual Local Dev (Using `uv`)
Use this if you want to run the Python code directly on your machine for debugging.

1.  **Prerequisites:** You must have MongoDB and Redis running locally (or use Cloud URIs).

2.  **Install Dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the Server:**
    ```bash
    uv run uvicorn backend.main:app --reload
    ```

## 🖥️ Frontend Setup
Since the frontend is static HTML/JS, you need to serve it separately to avoid CORS issues.

1.  Open a new terminal.
2.  Navigate to the frontend folder:
    ```bash
    cd frontend
    ```
3.  Start a simple Python HTTP server:
    ```bash
    python -m http.server 5500
    ```
4.  Open your browser to: **http://localhost:5500**

## 🧪 Benchmarking
To test the performance improvements from Redis Caching:

1.  Ensure the Docker stack is running.
2.  Run the benchmark script (requires `aiohttp`):
    ```bash
    uv run python benchmark.py
    ```
    *Target Performance: ~950+ RPS with caching enabled.*
