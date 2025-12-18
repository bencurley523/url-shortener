# Full-Stack URL Shortener

A RESTful API and frontend application that shortens URLs, handles redirections, and tracks usage, built with **FastAPI** and **MongoDB**.

## 🚀 Tech Stack

* **Backend:** Python 3.12+, FastAPI, Uvicorn
* **Database:** MongoDB Atlas (Cloud NoSQL)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Tooling:** `uv` (Modern Python package manager)

## ✨ Features

* **URL Shortening:** Fast generation of short codes for long URLs.
* **Custom Aliases:** Users can request specific custom short codes (e.g., `/my-link`).
* **Redirection:** Instant HTTP 307 redirects to the original URL.
* **Duplicate Handling:** Validates if an alias is already in use.
* **CORS Support:** Configured for secure local development and cross-origin requests.

## 🛠️ Setup & Installation

### 1. Clone the Repository
First, clone the project to your local machine and navigate into the directory.

```bash
git clone [https://github.com/bencurley523/url-shortener.git](https://github.com/bencurley523/url-shortener.git)
cd url-shortener
```

### 2. Configuration (.env)
You must set up your database connection before running the app.

1.  Create a file named `.env` in the root directory (`url-shortener/`).
2.  Paste your MongoDB connection string into it:
    ```env
    MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/myDatabase
    ```

### 3. Installation & Running
Choose **one** of the methods below.

#### Option A: Using `uv` (Recommended)
This project uses [uv](https://github.com/astral-sh/uv) for fast dependency management.

1.  **Sync dependencies:**
    ```bash
    uv sync
    ```
2.  **Run the server:**
    ```bash
    uv run uvicorn backend.main:app --reload
    ```

#### Option B: Using standard `pip`
If you do not have `uv`, you can use standard Python tools.

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the server:**
    ```bash
    uvicorn backend.main:app --reload
    ```

## 📂 Project Structure

```text
url-shortener/
├── backend/             # Backend Application Code
│   ├── __init__.py
│   ├── database.py      # Database connection logic
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # Pydantic models
│   ├── utils.py         # Utility methods
├── frontend/            # User Interface
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── .env                 # Secrets (Not committed to Git)
├── requirements.txt     # Dependencies for pip
├── pyproject.toml       # Dependencies for uv
└── README.md            # Project Documentation
```

## 📝 Usage

To run the full application, you will need two terminal windows open.

### 1. Start the Backend
In your first terminal, make sure the FastAPI server is running:
```bash
uv run uvicorn backend.main:app --reload
```
### 2. Start the Frontend
In a new terminal, serve the frontend files to avoid CORS issues:

```bash
cd frontend
python -m http.server 5500
```

### 3. Access the App

Open your browser and navigate to http://localhost:5500.

Enter a long URL (and optionally a custom alias).

Click Shorten to generate your link!