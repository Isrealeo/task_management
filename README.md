# Task Management API

A RESTful Task Management API built with **Django** and **Django REST Framework**.  
This API allows users to register, authenticate, create and manage tasks with priorities, due dates, filtering, ordering, and task sharing.

---

## 🚀 Features

### ✅ Authentication
- User registration
- Token-based login authentication
- Protected routes using authentication tokens

### ✅ Task Management
- Create, update, delete tasks
- Mark tasks as **completed** or **pending**
- Prevent editing of completed tasks
- Assign **priority** (Low, Medium, High)
- Set **due dates**
- Track completion time

### ✅ Advanced Task Features
- Filter tasks by:
  - status (`PENDING`, `COMPLETED`)
  - priority (`Low`, `Medium`, `High`)
- Order tasks by:
  - due date
  - priority
- Share tasks with other users
- Categorize tasks
- Optional recurrence (Daily, Weekly)

---

## 🛠 Tech Stack

- Python 3
- Django
- Django REST Framework
- Token Authentication
- SQLite (development)

---

## 📌 API Endpoints (Summary)

### Auth
- `POST /api/auth/register/` – Register user
- `POST /api/auth/login/` – Login & receive token

### Tasks
- `GET /api/tasks/` – List user tasks
- `POST /api/tasks/` – Create task
- `GET /api/tasks/{id}/` – Retrieve task
- `PUT /api/tasks/{id}/` – Update task
- `DELETE /api/tasks/{id}/` – Delete task
- `PATCH /api/tasks/{id}/revert/` – Revert completed task

### Query Parameters

---

## 🔐 Authentication Usage

All task endpoints require authentication.

Include token in headers:


---

## 🧪 Testing

- Tested using **Postman**
- Supports GET, POST, PUT, PATCH, DELETE requests
- Token-based authorization enabled

---

## 📦 Deployment

- Deployment-ready for platforms like **PythonAnywhere**
- Virtual environment supported
- WSGI configuration required for production

---

## 👤 Author

**Isreal Nwaminogbe**

---

## 📄 License

This project is for educational purposes.
