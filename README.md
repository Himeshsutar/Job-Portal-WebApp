# Job-Portal-WebApp
# 💼 Job Portal Web Application

A full-featured web application where **Job Seekers** can search and apply for jobs, while **Employers** can post and manage job listings. Built using Django, this project demonstrates core full-stack development skills.

---

## 🚀 Features

### 👤 User Roles
- **Job Seeker**
  - Register and log in
  - Search and filter job listings
  - Apply to jobs (only once per job)
  

- **Employer**
  - Register and log in
  - Post new job listings
  - View, edit, and delete job posts

- **Admin**
  - Access Django Admin Panel
  - Manage all users, jobs, and applications

---

### ✅ Core Functionalities
- User Registration and Login
- Role-based Access Control
- Job Posting with:
  - Title, Description, Location, Salary
- Search and Filtering:
  - Search by title, location, company
- Prevent duplicate job applications
- Separate dashboards for each user type

---

## 📁 Project Structure

```
Job-Portal-WebApp/
│
├── jobapp/
│   ├── __pycache__/
│   ├── migrations/
│   ├── static/
│   │   └── jobapp/
│   │       └── style.css
│   ├── templates/
│   │   └── jobapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
├── resumes/
├── staticfiles/              # Generated after running collectstatic
│
├── .env                      # Environment variables
├── .gitignore
├── asgi.py
├── db.sqlite3
├── manage.py
├── Procfile
├── README.md
├── requirements.txt
├── settings.py
├── urls.py
└── wsgi.py

```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Himeshsutar/Job-Portal-WebApp.git
cd job-portal-webapp
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Create a Superuser (Admin access)
```bash
python manage.py createsuperuser
```

### 5️⃣ Run the Development Server
```bash
python manage.py runserver
```

---

## 🔗 Live Deployment

The application is live at:  
👉 https://job-portal-webapp-kbrn.onrender.com

🛈 **Note**: Hosted on Render’s free plan.  
Free services **go to sleep after inactivity**, so initial page loads may be **slightly delayed** (cold start). Subsequent usage will be smooth.


## 📌 Project Highlights

- Fully role-based navigation and views
- Custom dashboards for Employers and Job Seekers
- Clean and modular codebase following Django best practices
- Simple and responsive UI using Bootstrap
- Validations for duplicate applications and restricted access

---

⭐ *Thank you for reviewing my project!*
