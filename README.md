<div align="center">

# 🧾 ResumeForge

### Build professional ATS-friendly resumes in minutes

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![PythonAnywhere](https://img.shields.io/badge/Hosted_on-PythonAnywhere-blue?style=flat-square)

<br/>

![ResumeForge Banner](https://img.shields.io/badge/ResumeForge-Resume%20Builder%20Web%20App-16a34a?style=for-the-badge)

</div>

---

## ✨ Features

- 📝 **Multi-step resume builder** with auto-save
- 🎨 **4 professional templates** — Modern, Minimal, Corporate, Creative
- 📄 **PDF download** via WeasyPrint
- 🔐 **Email OTP verification** on register
- 🔑 **Google OAuth login**
- 📊 **Dashboard** to manage multiple resumes
- 🖼️ **Photo upload** support
- 📱 **Responsive** design

---

## 📁 Project Structure

```
mysite/
├── 📂 mysite/                  # Django project core
│   ├── settings.py             # All configuration
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py                 # WSGI entry point
│
├── 📂 resume/                  # Resume builder app
│   ├── models.py               # Resume model
│   ├── views.py                # All resume views
│   ├── urls.py                 # Resume URLs
│   ├── templatetags/
│   │   └── resume_tags.py      # Custom template filters
│   ├── migrations/
│   └── templates/resume/
│       ├── landing.html        # Landing page
│       ├── dashboard.html      # User dashboard
│       ├── build.html          # Resume builder UI
│       ├── pdf_preview.html    # PDF render template
│       └── partials/
│           ├── resume_body.html # Resume HTML structure
│           └── resume_css.html  # Resume styles
│
├── 📂 accounts/                # Auth app
│   ├── models.py               # UserProfile, OTPCode
│   ├── views.py                # Register, Login, OTP, Google OAuth
│   ├── forms.py                # Auth forms
│   ├── urls.py                 # Auth URLs
│   └── templates/accounts/
│
├── 📂 main/                    # Portfolio landing page
├── 📂 converter/               # Unit converter (optional)
├── 📂 media/                   # Uploaded photos
├── 📂 staticfiles/             # Collected static files
├── manage.py
├── requirements.txt
├── pythonanywhere_wsgi_TEMPLATE.py
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites

Make sure you have these installed:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| pip | latest | comes with Python |
| Git | any | [git-scm.com](https://git-scm.com/) |

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/resumeforge.git
cd resumeforge/mysite
```

---

### Step 2 — Create virtual environment

```bash
# Create venv
python -m venv venv

# Activate — Linux/macOS
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

---

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> **WeasyPrint** also needs system-level libraries for PDF generation:

```bash
# Ubuntu / Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0

# macOS (with Homebrew)
brew install pango

# Windows — WeasyPrint can be tricky on Windows.
# Use xhtml2pdf as fallback (already in requirements.txt)
# Or use WSL (Windows Subsystem for Linux)
```

---

### Step 4 — Configure credentials

Open `mysite/settings.py` and fill in these sections:

#### 📧 Email (Gmail SMTP) — for OTP verification

```python
# mysite/settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_gmail@gmail.com'        # ← your Gmail address
EMAIL_HOST_PASSWORD = 'your_app_password_here'  # ← Gmail App Password (NOT your login password)
DEFAULT_FROM_EMAIL = 'ResumeForge <your_gmail@gmail.com>'
```

> **How to get a Gmail App Password:**
> 1. Go to [myaccount.google.com](https://myaccount.google.com)
> 2. Security → 2-Step Verification → App Passwords
> 3. Select **Mail** → Generate
> 4. Copy the 16-character password

#### 🔑 Google OAuth — for "Continue with Google" button

```python
# mysite/settings.py

GOOGLE_CLIENT_ID = 'your_client_id.apps.googleusercontent.com'  # ← from Google Console
GOOGLE_CLIENT_SECRET = 'your_client_secret'                      # ← from Google Console
```

> **How to create Google OAuth credentials:**
> 1. Go to [console.cloud.google.com](https://console.cloud.google.com)
> 2. Create a project (or select existing)
> 3. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
> 4. Application type: **Web application**
> 5. Add **Authorised JavaScript origins**:
>    ```
>    http://localhost:8000
>    ```
> 6. Add **Authorised redirect URIs**:
>    ```
>    http://localhost:8000/accounts/google/callback/
>    ```
> 7. Click **Create** → copy the **Client ID** and **Client Secret**

#### 🔒 Secret Key

```python
# mysite/settings.py

SECRET_KEY = 'replace-this-with-a-long-random-string'
```

> Generate one here: [djecrety.ir](https://djecrety.ir/) or run:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

### Step 5 — Run migrations

```bash
python manage.py migrate
```

---

### Step 6 — Create admin user (optional)

```bash
python manage.py createsuperuser
```

---

### Step 7 — Run the server

```bash
python manage.py runserver
```

Open your browser → **http://127.0.0.1:8000/resumeforge/**

---

## ☁️ Deploy to PythonAnywhere

### Step 1 — Upload project

Upload the entire `mysite/` folder to:
```
/home/YOUR_USERNAME/mysite/
```

Use the PythonAnywhere **Files** tab to upload a zip, then extract:
```bash
cd ~
unzip mysite.zip
```

---

### Step 2 — Install dependencies

In PythonAnywhere **Bash console**:
```bash
pip install -r ~/mysite/requirements.txt --user
pip install weasyprint --user
pip install social-auth-app-django --user
```

---

### Step 3 — Run migrations

```bash
cd ~/mysite
python manage.py migrate
python manage.py collectstatic
```

---

### Step 4 — Configure WSGI file

In PythonAnywhere → **Web tab** → click the **WSGI configuration file** link.

Replace the entire content with the template below (already in `pythonanywhere_wsgi_TEMPLATE.py`):

```python
import os
import sys

project_home = '/home/YOUR_USERNAME/mysite'   # ← replace YOUR_USERNAME
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Email
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'your_gmail@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your_app_password'
os.environ['DEFAULT_FROM_EMAIL'] = 'ResumeForge <your_gmail@gmail.com>'

# Google OAuth
os.environ['GOOGLE_CLIENT_ID'] = 'your_client_id.apps.googleusercontent.com'
os.environ['GOOGLE_CLIENT_SECRET'] = 'your_client_secret'

# Security
os.environ['SECRET_KEY'] = 'your-long-random-secret-key'
os.environ['ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

### Step 5 — Static files mapping

In PythonAnywhere → **Web tab** → **Static files** section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/mysite/staticfiles/` |
| `/media/` | `/home/YOUR_USERNAME/mysite/media/` |

---

### Step 6 — Google OAuth redirect URI for production

Go back to [Google Cloud Console](https://console.cloud.google.com) → your OAuth client → **Edit** → add:

**Authorised JavaScript origins:**
```
https://YOUR_USERNAME.pythonanywhere.com
```

**Authorised redirect URIs:**
```
https://YOUR_USERNAME.pythonanywhere.com/accounts/google/callback/
```

---

### Step 7 — Reload

Click the green **Reload** button in PythonAnywhere Web tab.

Your app is live at:
```
https://YOUR_USERNAME.pythonanywhere.com/resumeforge/
```

---

## 🌐 URL Structure

| URL | Page |
|-----|------|
| `/` | Portfolio homepage |
| `/resumeforge/` | ResumeForge landing page |
| `/resumeforge/dashboard/` | User dashboard |
| `/resumeforge/resume/new/` | Create new resume |
| `/resumeforge/resume/<id>/build/` | Resume builder |
| `/resumeforge/resume/<id>/download/` | Download PDF |
| `/accounts/register/` | Register |
| `/accounts/login/` | Login |
| `/accounts/google/` | Google OAuth |
| `/admin/` | Django admin |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| PDF Generation | WeasyPrint |
| Auth | Django Auth + OTP + Google OAuth |
| Frontend | HTML, CSS, Vanilla JS |
| Hosting | PythonAnywhere |
| Email | Gmail SMTP |

---

## ⚠️ Common Issues

**`no such table` error after deploy**
```bash
cd ~/mysite && python manage.py migrate
```

**PDF not downloading**
```bash
pip install weasyprint --user
```

**Google login shows "not configured"**
→ Make sure `GOOGLE_CLIENT_ID` is set in the WSGI file and the redirect URI matches exactly.

**OTP email not sending**
→ Check that `EMAIL_HOST_PASSWORD` is a Gmail **App Password**, not your Gmail login password.

**Static files not loading**
```bash
python manage.py collectstatic
```
Then add the static files mapping in PythonAnywhere Web tab.

---

## 👨‍💻 Author

**Arjun Krishnan P.S**

[![GitHub](https://img.shields.io/badge/GitHub-axxor06-181717?style=for-the-badge&logo=github)](https://github.com/axxor06)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Arjun_Krishnan-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/arjun-krishnan)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-16a34a?style=for-the-badge&logo=google-chrome&logoColor=white)](https://arjunkrishnanps.pythonanywhere.com)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Made with ❤️ using Django
<h2>Live = https://arjunkrishnanps.pythonanywhere.com/resumeforge/ </h2>
</div>
