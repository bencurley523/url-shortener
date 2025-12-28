# High-Performance Async URL Shortener

A high-concurrency, distributed URL shortener engineered for speed and scalability. It uses an **asynchronous microservices architecture** orchestrated by **Kubernetes**, featuring **Redis caching** for sub-millisecond read times, Nginx load balancing, and a fully containerized deployment.

## 🚀 Tech Stack

* **Backend:** Python 3.12+, FastAPI, Uvicorn, Motor (Async MongoDB Driver)
* **Frontend:** HTML5, CSS3, JavaScript (Served via Nginx)
* **Database:** MongoDB (StatefulSet / Persistent Volume)
* **Caching:** Redis (Cache-Aside pattern)
* **Infrastructure:** Kubernetes (K8s), Docker
* **Orchestration:** Deployment, Service, ConfigMap, Horizontal Pod Autoscaling

## ✨ Features

* **⚡ High Performance:** Capable of handling **1,500+ RPS** locally via load-balanced backend replicas and Redis caching.
* **☁️ Cloud Native:** Fully distributed microservices architecture running on Kubernetes.
* **⚖️ Scalable:** Zero-downtime horizontal scaling (`kubectl scale`) to handle traffic spikes.
* **🛡️ Self-Healing:** Kubernetes automatically restarts crashed pods to ensure high availability.
* **🔄 Async Architecture:** Non-blocking I/O for database operations and request handling.
* **📊 Analytics:** Tracks click counts and timestamps asynchronously (Fire-and-forget).

## 📂 Project Structure

```
url-shortener/
├── backend/                # Backend Microservice
│   ├── Dockerfile          # Python 3.12 Slim Image
│   ├── main.py             # FastAPI Entrypoint
│   ├── models.py           # Data Models
│   ├── database.py         # Database Initialization
│   ├── crud.py             # Database Logic
│   ├── utils.py            # Base62 Encode
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/               # Frontend Microservice
│   ├── Dockerfile          # Nginx Alpine Image
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── k8s/                    # Kubernetes Manifests
│   ├── backend.yaml        # Deployment + LoadBalancer
│   ├── frontend.yaml       # Deployment + LoadBalancer
│   └── database.yaml       # Mongo & Redis Services
│
├── benchmark.py            # Async Load Testing Script
└── README.md
```

## 🛠️ Setup & Deployment

We use **Kubernetes** to orchestrate the application. Since we use official images for MongoDB and Redis, you only need to build the custom images for the backend and frontend.

*Requires: Docker Desktop (Kubernetes enabled)*

### 1. Build Custom Images
We need to package your Python and HTML code into images so Kubernetes can use them.
```
docker build -t url-shortener-backend:latest ./backend
docker build -t url-shortener-frontend:latest ./frontend
```

### 2. Deploy to Kubernetes
This command tells Kubernetes to create the Deployment and Services for all components (Backend, Frontend, Mongo, Redis).
```
kubectl apply -f k8s/
```

### 3. Verify & Access
Wait until all pods show status `Running`.
```
kubectl get pods
```

Once running, access the services locally:
* **Frontend UI:** [http://localhost:3000](http://localhost:3000)
* **Backend API:** [http://localhost:8000](http://localhost:8000)

### 4. Scaling (Optional)
To handle higher traffic loads, you can instantly spin up more backend replicas:
```
kubectl scale deployment backend-deployment --replicas=5
```

## 🧪 Benchmarking
To stress-test the distributed system, use the provided async script. This requires `uv` to handle dependencies.

1.  **Run the benchmark:**
    ```
    uv run benchmark.py
    ```

    *Note: If you haven't synced dependencies yet, run `uv sync` first.*

## 🧹 Cleanup
To remove all resources and stop the cluster:
<CODE>
kubectl delete -f k8s/
</CODE>