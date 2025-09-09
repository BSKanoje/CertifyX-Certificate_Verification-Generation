# CertifyX - SaaS Platform for Internship Certificate Generation & Verification

## Problem Statement

### The Current Problem
Currently, when students complete an internship, companies usually provide them a certificate as proof of completion. But in many cases, this certificate is created manually using Word or design tools. Here’s how it usually works:

1. The company types out each student’s name and other details manually in a Word file.
2. They generate a PDF for each certificate.
3. A unique ID is assigned manually to each certificate.
4. The company emails or shares the certificate individually with each student.
5. There is no proper tracking of how many certificates have been created or shared.
6. If someone wants to verify whether a certificate is genuine, they must call or email the company — there is no easy way to do it online.

This manual process is slow, tiring, and completely dependent on a single person in the company. If that person is on leave or unavailable, the certificate work gets blocked. Additionally, as the number of students increases, it becomes very difficult to handle this manually. Moreover, if multiple people across different departments want to generate certificates at the same time, it is not possible. This makes the system non-scalable, creating delays and confusion.

### Major Pain Points
- Time-consuming manual process
- Human-dependent, leading to delays
- Difficult to track or manage certificate records
- No way to verify certificates online
- Non-scalable as the number of certificates increases
- No reports or dashboards to see how many certificates have been issued, pending, etc.

## What We Want to Build

To solve this problem, we want to build a SaaS-based (Software as a Service) platform that automates the entire process of certificate generation.

### Features & Functional Modules
1. **Authentication & User Management**  
   - Register an account with basic info like company name, email, phone number, and password.
   - Login/logout securely.
   - Reset password with optional admin approval for new companies.

2. **Subscription & Pricing Plans**  
   - Multiple pricing tiers based on the number of certificates needed monthly.
   - Payment integration (mock payment gateway).

3. **Template Management**  
   - Companies can upload custom certificate templates.
   - Define dynamic fields (e.g., Name, Course, Date).

4. **Candidate Management (CRUD)**  
   - Add candidates manually or upload bulk data via Excel.
   - View, edit, and delete candidate records.

5. **Certificate Generation**  
   - Auto-generate certificates with unique IDs and QR codes.
   - Certificates are downloadable or sent via email.

6. **Certificate Verification**  
   - Public page for certificate verification by entering ID or scanning QR code.

7. **Dashboard & Reporting**  
   - Dashboard for tracking certificate usage, remaining quotas, and templates used.
   - Reports with charts and usage statistics.

8. **Profile & Account Settings**  
   - Companies can update their profile, view subscription details, and change passwords.

9. **Admin Panel (Super Admin)**  
   - Manage all company accounts and subscription plans.
   - Track company certificate usage and manage reports.

## Target Users
- **Super Admin (Platform Owner)**: Manages platform settings, billing, user issues.
- **Company Admin (Client)**: Manages templates, certificate generation, team access.
- **Recipient / Verifier**: Receives certificates or visits the platform to verify authenticity.

## Tech Stack
- **Backend**: Python + Django
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Database**: MySQL
- **Versioning**: Git + GitHub
- **File Storage**: Local/Cloud (initially local file system for certs)
- **Payments**: Razorpay/Stripe/Paypal (mocked for now)
- **QR Generator**: Python library like `qrcode`
- **PDF Generator**: Reportlab/WeasyPrint/wkhtmltopdf

## Bonus Features (Optional)
- Auto-email with PDF attachment
- Role-based access to certificate generation for company teams
- Expiry alerts to company email

## ⚙️ Installation & Setup

Follow these steps to set up CertifyX on your local machine:

### 1️⃣ Prerequisites
- Python 3.9+ installed ([Download here](https://www.python.org/downloads/))
- Git installed ([Download here](https://git-scm.com/downloads))

> **Optional:** Install MySQL if you want to use it in production ([Download here](https://dev.mysql.com/downloads/installer/)).

### 2️⃣ Clone Repository
```bash
git clone https://github.com/your-username/certifyx.git
cd certifyx
```
### 3️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```
### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 5️⃣ Configure Database

✅ Default (SQLite)
The project uses SQLite by default. No setup needed.
settings.py already contains:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
🔄 Switch to MySQL (Optional)
If you want to use MySQL, update settings.py:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'certifyx_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6️⃣ Create Superuser
```bash
python manage.py createsuperuser
```
### 7️⃣ Run Development Server
```bash
python manage.py runserver
```
Now open http://127.0.0.1:8000/ in your browser to view the project.

## 📂 Project Structure

```plaintext
Certificate-Generation.Verification-main/
├── accounts/            # Handles company registration, authentication, login/logout
├── candidates/          # Candidate CRUD (Create, Read, Update, Delete) operations
├── generateCertificate/ # Core certificate generation logic (PDF, QR code)
├── manageTemplate/      # Upload, edit, and manage certificate templates
├── main/                # Main project settings and URLs
├── media/               # Uploaded templates, logos, and generated certificates
├── subscriptions/       # Subscription plans and usage tracking
├── db.sqlite3           # Default SQLite database file
├── manage.py            # Django management commands
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── Pipfile / Pipfile.lock # (Optional) Virtual environment dependency management
└── .gitignore           # Git ignored files and folders
```
