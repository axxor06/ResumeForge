# ResumeForge — Django Resume Builder

A Django web app for building and downloading ATS-friendly resumes.
Hosted at: https://YOUR_USERNAME.pythonanywhere.com/resumeforge/

---

## Features
- Register / Login with email + OTP verification
- Google OAuth login
- 4 resume templates (Modern, Minimal, Corporate, Creative)
- Auto-save while building
- PDF download via WeasyPrint
- Dashboard to manage multiple resumes

---

## Project Structure

```
mysite/
├── mysite/          # Django project settings, urls, wsgi
├── resume/          # Resume builder app
├── accounts/        # Auth app (register, login, OTP, Google OAuth)
├── main/            # Portfolio/landing page app
├── media/           # Uploaded photos
├── staticfiles/     # Collected static files
├── manage.py
├── requirements.txt
└── pythonanywhere_wsgi_TEMPLATE.py
```

---

## Local Setup

### 1. Clone / extract the project
```bash
cd ~
# extract zip here
cd mysite
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

WeasyPrint also needs system libraries:
```bash
# Ubuntu / Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0

# macOS
brew install pango
```

### 4. Configure settings
Edit `mysite/settings.py` and set:
- `SECRET_KEY` — any long random string
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` — Gmail + App Password
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — from Google Cloud Console

Or set them as environment variables.

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Collect static files
```bash
python manage.py collectstatic
```

### 8. Run dev server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/resumeforge/

---

## PythonAnywhere Deployment

### 1. Upload project
Upload the entire `mysite/` folder to `/home/YOUR_USERNAME/mysite/`

### 2. Install dependencies
In PythonAnywhere Bash console:
```bash
pip install -r ~/mysite/requirements.txt --user
pip install weasyprint --user
pip install social-auth-app-django --user
```

### 3. Configure WSGI
- Go to PythonAnywhere → Web tab
- Click the WSGI configuration file link
- Replace its contents with `pythonanywhere_wsgi_TEMPLATE.py`
- Fill in your username, Gmail, and Google credentials

### 4. Static files mapping
In PythonAnywhere Web tab → Static files:
| URL         | Directory                              |
|-------------|----------------------------------------|
| /static/    | /home/YOUR_USERNAME/mysite/staticfiles/|
| /media/     | /home/YOUR_USERNAME/mysite/media/      |

### 5. Run migrations
```bash
cd ~/mysite
python manage.py migrate
python manage.py collectstatic
```

### 6. Reload the app
Click the green Reload button in PythonAnywhere Web tab.

---

## Google OAuth Setup

1. Go to https://console.cloud.google.com
2. Create a project → APIs & Services → Credentials
3. Create OAuth 2.0 Client ID (Web application)
4. Authorised JavaScript origins: `https://YOUR_USERNAME.pythonanywhere.com`
5. Authorised redirect URIs: `https://YOUR_USERNAME.pythonanywhere.com/accounts/google/callback/`
6. Copy Client ID and Secret into WSGI file or settings.py

---

## Gmail App Password Setup

1. Go to Google Account → Security → 2-Step Verification → App Passwords
2. Create an app password for "Mail"
3. Use that 16-character password as `EMAIL_HOST_PASSWORD`

---

## Main app (Portfolio)

The `main` app serves your portfolio at `/`.
Replace `main/templates/main/index.html` with your portfolio HTML.

---

## Notes
- `converter/` app — Unit converter, include/exclude in `mysite/urls.py` as needed
- All sections in the resume are optional — empty ones won't appear in PDF
- PDF uses WeasyPrint. If not installed, falls back to xhtml2pdf, then browser print
