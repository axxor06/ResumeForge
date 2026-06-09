import os
import sys

# ── PATH ──────────────────────────────────────────────────────
# Replace YOUR_USERNAME with your PythonAnywhere username
project_home = '/home/YOUR_USERNAME/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ── SETTINGS ──────────────────────────────────────────────────
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# ── EMAIL (Gmail SMTP) ────────────────────────────────────────
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'your_gmail@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'your_gmail_app_password'
os.environ['DEFAULT_FROM_EMAIL'] = 'ResumeForge <your_gmail@gmail.com>'

# ── GOOGLE OAUTH ──────────────────────────────────────────────
os.environ['GOOGLE_CLIENT_ID'] = 'your_google_client_id.apps.googleusercontent.com'
os.environ['GOOGLE_CLIENT_SECRET'] = 'your_google_client_secret'

# ── SECURITY ──────────────────────────────────────────────────
os.environ['SECRET_KEY'] = 'replace-with-a-long-random-secret-key'
os.environ['ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
