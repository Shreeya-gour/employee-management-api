# Employee Management REST API 🚀

A robust, enterprise-grade Employee Management REST API built with **Python**, **Django**, and **Django REST Framework (DRF)**.

---

## 📌 Features

- **Full CRUD Operations**: Create, Read, Update (PUT & PATCH), and Delete employee records.
- **SQLite with Django ORM**: Relational schema mapping with field-level constraints (`unique`, `decimal`, `date`).
- **Data Validation**: Custom field validations for name, positive salary, and duplicate email prevention.
- **Clean Architecture**:
  - `APIView` for granular low-level endpoint logic.
  - `GenericAPIView` & Mixins for standardized CRUD.
  - `ModelViewSet` and `DefaultRouter` for production-level routing.
- **Filtering, Search & Pagination**:
  - Case-insensitive department filtering (`?department=Engineering`).
  - Multi-field keyword search across name and email (`?search=shreeya`).
  - Dynamic sorting/ordering (`?ordering=-salary`).
  - Custom page-number pagination envelope (`count`, `next`, `previous`, `results`).
- **Security & Permissions**:
  - `SessionAuthentication` & `BasicAuthentication`.
  - `IsAuthenticatedOrReadOnly` permission rules (safe public reads, authenticated writes).
- **Automated Testing**: 100% test coverage using DRF `APITestCase`.
- **Django Admin Panel**: Customized GUI dashboard with search and filters.

---

## 🛠️ Tech Stack

- **Language:** Python 3.15
- **Framework:** Django 6.1, Django REST Framework 3.18
- **Database:** SQLite3
- **Testing:** Django `TestCase`, DRF `APITestCase`
- **Version Control:** Git & GitHub

---

## 🚀 Quickstart Guide

### 1. Clone the repository
```bash
git clone <your-github-repo-url>
cd CrudProject
```

### 2. Create & Activate Virtual Environment
```powershell
python -m venv env
.\env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Start the Server
```bash
python manage.py runserver
```
Visit the interactive Browsable API at: `http://127.0.0.1:8000/api/`  
Visit the Admin Panel at: `http://127.0.0.1:8000/admin/`

---

## 🧪 Run Automated Tests
```bash
python manage.py test
```

---

## 📡 API Endpoints Reference

| HTTP Method | Endpoint | Description | Auth Required? |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/employees/` | List all employees (paginated) | No |
| `GET` | `/api/employees/?search=<query>` | Search employees by name or email | No |
| `GET` | `/api/employees/?department=<dept>` | Filter employees by department | No |
| `GET` | `/api/employees/?ordering=-salary` | Sort employees by salary descending | No |
| `POST` | `/api/employees/` | Create a new employee | **Yes** (Basic / Session) |
| `GET` | `/api/employees/<id>/` | Retrieve employee by ID | No |
| `PUT` | `/api/employees/<id>/` | Full update employee record | **Yes** (Basic / Session) |
| `PATCH` | `/api/employees/<id>/` | Partial update employee fields | **Yes** (Basic / Session) |
| `DELETE` | `/api/employees/<id>/` | Delete employee record | **Yes** (Basic / Session) |
