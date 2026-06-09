import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import UserProfile, OTPCode
from .forms import RegisterForm, LoginForm, OTPForm, ForgotPasswordForm, ResetPasswordForm


def _send_otp_email(user, otp_obj):
    subject = "Your ResumeForge verification code"
    if otp_obj.purpose == OTPCode.PURPOSE_RESET:
        subject = "Your ResumeForge password reset code"
    body = f"""
Hi {user.first_name or user.username},

Your ResumeForge verification code is:

  {otp_obj.code}

This code expires in {getattr(settings, 'OTP_EXPIRY_MINUTES', 10)} minutes.
If you didn't request this, please ignore this email.

— The ResumeForge Team
"""
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    except Exception:
        pass


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        username = cd['email'].split('@')[0]
        base = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1
        user = User.objects.create_user(
            username=username,
            email=cd['email'],
            password=cd['password'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
            is_active=True,
        )
        UserProfile.objects.get_or_create(user=user, defaults={"is_email_verified": False})
        otp = OTPCode.generate_for(user, OTPCode.PURPOSE_VERIFY)
        _send_otp_email(user, otp)
        request.session['pending_verify_uid'] = user.pk
        messages.success(request, f"Account created! We sent a 6-digit code to {user.email}")
        return redirect('verify_email')
    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request):
    uid = request.session.get('pending_verify_uid')
    if not uid:
        return redirect('login')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return redirect('login')

    form = OTPForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['otp'].strip()
        otp = OTPCode.objects.filter(user=user, purpose=OTPCode.PURPOSE_VERIFY, is_used=False).first()
        if otp and otp.is_valid() and otp.code == code:
            otp.is_used = True
            otp.save()
            user.profile.is_email_verified = True
            user.profile.save()
            del request.session['pending_verify_uid']
            login(request, user)
            messages.success(request, "Email verified! Welcome to ResumeForge 🎉")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
    return render(request, 'accounts/verify_email.html', {'form': form, 'email': user.email})


def resend_otp_view(request):
    uid = request.session.get('pending_verify_uid') or request.session.get('reset_uid')
    if not uid:
        return redirect('login')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return redirect('login')
    purpose = OTPCode.PURPOSE_RESET if 'reset_uid' in request.session else OTPCode.PURPOSE_VERIFY
    otp = OTPCode.generate_for(user, purpose)
    _send_otp_email(user, otp)
    messages.info(request, "A new code has been sent to your email.")
    if purpose == OTPCode.PURPOSE_RESET:
        return redirect('reset_otp')
    return redirect('verify_email')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        try:
            u = User.objects.get(email=cd['email'].lower())
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, 'accounts/login.html', {'form': form})
        user = authenticate(request, username=u.username, password=cd['password'])
        if user:
            if not cd.get('remember_me'):
                request.session.set_expiry(0)
            login(request, user)
            nxt = request.GET.get('next', 'dashboard')
            return redirect(nxt)
        else:
            messages.error(request, "Incorrect password.")
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('landing')


def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
            otp = OTPCode.generate_for(user, OTPCode.PURPOSE_RESET)
            _send_otp_email(user, otp)
            request.session['reset_uid'] = user.pk
        except User.DoesNotExist:
            pass
        messages.success(request, f"If an account exists for {email}, we sent a reset code.")
        return redirect('reset_otp')
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_otp_view(request):
    uid = request.session.get('reset_uid')
    if not uid:
        return redirect('forgot_password')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return redirect('forgot_password')

    form = OTPForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data['otp'].strip()
        otp = OTPCode.objects.filter(user=user, purpose=OTPCode.PURPOSE_RESET, is_used=False).first()
        if otp and otp.is_valid() and otp.code == code:
            otp.is_used = True
            otp.save()
            request.session['reset_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid or expired code.")
    return render(request, 'accounts/reset_otp.html', {'form': form, 'email': user.email})


def reset_password_view(request):
    uid = request.session.get('reset_uid')
    if not uid or not request.session.get('reset_verified'):
        return redirect('forgot_password')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return redirect('forgot_password')

    form = ResetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user.set_password(form.cleaned_data['password'])
        user.save()
        del request.session['reset_uid']
        del request.session['reset_verified']
        messages.success(request, "Password updated! Please log in with your new password.")
        return redirect('login')
    return render(request, 'accounts/reset_password.html', {'form': form})


def google_login_view(request):
    """Redirect to Google OAuth — basic implementation; swap for python-social-auth in prod."""
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    if not client_id:
        messages.warning(request, "Google Sign-In is not configured yet.")
        return redirect('login')
    redirect_uri = request.build_absolute_uri('/accounts/google/callback/')
    scope = 'openid email profile'
    google_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&access_type=offline"
    )
    return redirect(google_url)


def google_callback_view(request):
    code = request.GET.get('code')
    if not code:
        messages.error(request, "Google login failed.")
        return redirect('login')
    client_id = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', '')
    redirect_uri = request.build_absolute_uri('/accounts/google/callback/')
    try:
        token_resp = requests.post('https://oauth2.googleapis.com/token', data={
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }, timeout=10)
        tokens = token_resp.json()
        access_token = tokens.get('access_token')
        info_resp = requests.get('https://www.googleapis.com/oauth2/v2/userinfo',
                                 headers={'Authorization': f'Bearer {access_token}'}, timeout=10)
        info = info_resp.json()
        email = info.get('email', '').lower()
        google_id = info.get('id', '')
        first_name = info.get('given_name', '')
        last_name = info.get('family_name', '')
        avatar_url = info.get('picture', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user = User.objects.create_user(username=username, email=email,
                                            first_name=first_name, last_name=last_name,
                                            is_active=True)
            user.set_unusable_password()
            user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.google_id = google_id
        profile.avatar_url = avatar_url
        profile.is_email_verified = True
        profile.save()
        login(request, user)
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, "Google login failed. Please try again.")
        return redirect('login')
