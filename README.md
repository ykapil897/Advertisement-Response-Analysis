# Advertisement Response Analysis Project

## Introduction
This project analyzes advertisement responses using a **Django backend** and a **Vite+React frontend**. It includes scripts to load, clean, and transform data, which are executed within Docker containers. Data is stored in a **MongoDB database**, and the project can be run with or without Docker by adjusting the MongoDB connection strings.

---

## Directory Structure

```plaintext
project-root/
├── backend/
├── frontend/
├── scripts/
│   ├── ext_and_load.py
│   ├── ld_gform_responses.py
│   └── clean_and_transform.py
└── docker-compose.yml
```

## How It Works

- **Backend (Django):** Serves API endpoints for data handling.
- **Frontend (Vite+React):** Provides a user interface to interact with the project.
- **Data Loading and Transformation Scripts:**
  - **ext_and_load.py**: Loads data from an Excel file into MongoDB.
  - **ld_gform_responses.py**: Loads new entries from Google Forms into MongoDB.
  - **clean_and_transform.py**: Cleans and transforms data, storing results in MongoDB.

---

## Initialization

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- A **MongoDB** instance, either locally or in a Docker container.

---

### Steps to Initialize the Project

1. **Clone the Repository:**

```bash
git clone <repository_url>
cd <repository_name>
```

2. **Set Up Environment Variables:**  
   Create a `.env` file in the root directory with the following content:

```plaintext
MONGO_URI=<your_mongodb_uri>
```

### 3. Modify MongoDB Connection Strings
Adjust the MongoDB connection strings in the scripts (`ext_and_load.py`, `ld_gform_responses.py`, `clean_and_transform.py`) depending on your environment:

- **For Docker:** Use the following connection string:
```plaintext
mongodb://172.17.0.1:27017
```
- **For Without Docker:** Use your MongoDB instance's URI, typically:
```plaintext
mongodb://127.0.0.1:27017
```

### 4. Build and Run Docker Containers
- To build and run the Docker containers, execute the following command:

```
docker-compose up --build
```

### 5. Access the Frontend

Open your browser and navigate to [http://localhost:5173](http://localhost:5173).

### 6. Access the Backend

The Django backend will be running at [http://localhost:8000](http://localhost:8000).

---

## Important Notes

- **Data Persistence:** The `tmp` directory is mounted as a volume in the Docker containers to persist temporary files.
- **Running Scripts:** The scripts (`ext_and_load.py`, `ld_gform_responses.py`, and `clean_and_transform.py`) are executed within Docker containers as defined in the `docker-compose.yml` file.
- **Environment Configuration:** Ensure that environment variables and MongoDB connection strings are correctly set up before running the project.

---

## Docker Compose Services

- **runner:** Runs the `run_all.py` script once.
- **scheduler:** Runs the `ld_gform_responses.py` script every 2 minutes.
- **transformer:** Runs the `clean_and_transform.py` script every 5 minutes.
- **frontend:** Runs the React frontend.
- **backend:** Runs the Django backend.