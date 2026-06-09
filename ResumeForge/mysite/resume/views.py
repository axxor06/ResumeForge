import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Resume


def landing(request):
    return render(request, 'resume/landing.html')


@login_required
def dashboard(request):
    q = request.GET.get('q', '').strip()
    resumes = request.user.resumes.all()
    if q:
        resumes = resumes.filter(title__icontains=q) | resumes.filter(full_name__icontains=q)
    return render(request, 'resume/dashboard.html', {'resumes': resumes, 'search_query': q})


@login_required
def create_resume(request):
    resume = Resume.objects.create(user=request.user, title='Untitled Resume', is_draft=True)
    return redirect('build_resume', pk=resume.pk)


@login_required
def build_resume(request, pk=None):
    if pk:
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
    else:
        resume = Resume.objects.create(user=request.user, title='Untitled Resume', is_draft=True)
        return redirect('build_resume', pk=resume.pk)
    return render(request, 'resume/build.html', {
        'resume': resume,
        'resume_json': json.dumps(resume.to_dict()),
    })


@login_required
def preview_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resume/pdf_preview.html', {'resume': resume})


@login_required
@require_POST
def save_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        resume.title     = data.get('title', resume.title) or 'Untitled Resume'
        resume.template  = data.get('template', resume.template)
        resume.full_name = data.get('full_name', '')
        resume.email     = data.get('email', '')
        resume.phone     = data.get('phone', '')
        resume.location  = data.get('location', '')
        resume.linkedin  = data.get('linkedin', '')
        resume.github    = data.get('github', '')
        resume.website   = data.get('website', '')
        resume.twitter   = data.get('twitter', '')
        resume.summary   = data.get('summary', '')
        resume.set_education(data.get('education', []))
        resume.set_experience(data.get('experience', []))
        resume.set_skills(data.get('skills', []))
        resume.set_soft_skills(data.get('soft_skills', []))
        resume.set_projects(data.get('projects', []))
        resume.set_certifications(data.get('certifications', []))
        resume.set_languages(data.get('languages', []))
        resume.set_achievements(data.get('achievements', []))
        resume.set_courses(data.get('courses', []))
        resume.set_volunteer(data.get('volunteer', []))
        resume.set_extracurricular(data.get('extracurricular', []))
        resume.set_references(data.get('references', []))
        resume.set_hobbies(data.get('hobbies', []))
        resume.is_draft = data.get('is_draft', False)
        resume.save()
        return JsonResponse({'status': 'ok', 'updated_at': resume.updated_at.strftime('%H:%M')})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def upload_photo(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    photo = request.FILES.get('photo')
    if not photo:
        return JsonResponse({'status': 'error', 'message': 'No photo provided'}, status=400)
    if photo.size > 5 * 1024 * 1024:
        return JsonResponse({'status': 'error', 'message': 'Max 5MB'}, status=400)
    if resume.photo:
        resume.photo.delete(save=False)
    resume.photo = photo
    resume.save()
    return JsonResponse({'status': 'ok', 'photo_url': resume.photo.url})


@login_required
@require_POST
def duplicate_resume(request, pk):
    o = get_object_or_404(Resume, pk=pk, user=request.user)
    Resume.objects.create(
        user=request.user, title=f"Copy of {o.title}", template=o.template,
        full_name=o.full_name, email=o.email, phone=o.phone, location=o.location,
        linkedin=o.linkedin, github=o.github, website=o.website, twitter=o.twitter,
        summary=o.summary,
        education_data=o.education_data, experience_data=o.experience_data,
        skills_data=o.skills_data, soft_skills_data=o.soft_skills_data,
        projects_data=o.projects_data, certifications_data=o.certifications_data,
        languages_data=o.languages_data, achievements_data=o.achievements_data,
        courses_data=o.courses_data, volunteer_data=o.volunteer_data,
        extracurricular_data=o.extracurricular_data, references_data=o.references_data,
        hobbies_data=o.hobbies_data,
    )
    messages.success(request, f'"{o.title}" duplicated.')
    return redirect('dashboard')


@login_required
@require_POST
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    title = resume.title
    resume.delete()
    messages.success(request, f'"{title}" deleted.')
    return redirect('dashboard')


@login_required
def download_pdf(request, pk):
    """Return a real downloadable PDF file."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    html_string = render_to_string('resume/pdf_preview.html', {
        'resume': resume, 'pdf_mode': True,
    }, request=request)

    safe_name = (resume.full_name or resume.title).replace(' ', '_')
    filename = f"{safe_name}_Resume.pdf"

    # Try WeasyPrint (best quality)
    try:
        from weasyprint import HTML
        pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(
            presentational_hints=True)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except ImportError:
        pass

    # Fallback: xhtml2pdf
    try:
        from xhtml2pdf import pisa
        import io
        buf = io.BytesIO()
        pisa.CreatePDF(html_string, dest=buf)
        response = HttpResponse(buf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except ImportError:
        pass

    # Last resort: render preview page (user can Ctrl+P → Save as PDF)
    return render(request, 'resume/pdf_preview.html', {'resume': resume})
