import json
from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('modern',    'Modern Professional'),
        ('minimal',   'Minimal Clean'),
        ('corporate', 'Corporate Classic'),
        ('creative',  'Creative Bold'),
    ]

    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title    = models.CharField(max_length=200, default='My Resume')
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='modern')

    full_name = models.CharField(max_length=200, blank=True)
    email     = models.EmailField(blank=True)
    phone     = models.CharField(max_length=30, blank=True)
    location  = models.CharField(max_length=200, blank=True)
    linkedin  = models.URLField(blank=True)
    github    = models.URLField(blank=True)
    website   = models.URLField(blank=True)
    twitter   = models.URLField(blank=True)
    summary   = models.TextField(blank=True)
    photo     = models.ImageField(upload_to='photos/', blank=True, null=True)

    declaration_place = models.CharField(max_length=200, blank=True)
    declaration_date  = models.CharField(max_length=100, blank=True)

    education_data       = models.TextField(default='[]')
    experience_data      = models.TextField(default='[]')
    skills_data          = models.TextField(default='[]')
    soft_skills_data     = models.TextField(default='[]')
    projects_data        = models.TextField(default='[]')
    certifications_data  = models.TextField(default='[]')
    languages_data       = models.TextField(default='[]')
    achievements_data    = models.TextField(default='[]')
    courses_data         = models.TextField(default='[]')
    volunteer_data       = models.TextField(default='[]')
    extracurricular_data = models.TextField(default='[]')
    references_data      = models.TextField(default='[]')
    hobbies_data         = models.TextField(default='[]')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_draft   = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} — {self.user.username}"

    def _get(self, f):    return json.loads(getattr(self, f) or '[]')
    def _set(self, f, v): setattr(self, f, json.dumps(v))

    def get_education(self):         return self._get('education_data')
    def set_education(self, v):      self._set('education_data', v)
    def get_experience(self):        return self._get('experience_data')
    def set_experience(self, v):     self._set('experience_data', v)
    def get_skills(self):            return self._get('skills_data')
    def set_skills(self, v):         self._set('skills_data', v)
    def get_soft_skills(self):       return self._get('soft_skills_data')
    def set_soft_skills(self, v):    self._set('soft_skills_data', v)
    def get_projects(self):          return self._get('projects_data')
    def set_projects(self, v):       self._set('projects_data', v)
    def get_certifications(self):    return self._get('certifications_data')
    def set_certifications(self, v): self._set('certifications_data', v)
    def get_languages(self):         return self._get('languages_data')
    def set_languages(self, v):      self._set('languages_data', v)
    def get_achievements(self):      return self._get('achievements_data')
    def set_achievements(self, v):   self._set('achievements_data', v)
    def get_courses(self):           return self._get('courses_data')
    def set_courses(self, v):        self._set('courses_data', v)
    def get_volunteer(self):         return self._get('volunteer_data')
    def set_volunteer(self, v):      self._set('volunteer_data', v)
    def get_extracurricular(self):   return self._get('extracurricular_data')
    def set_extracurricular(self, v):self._set('extracurricular_data', v)
    def get_references(self):        return self._get('references_data')
    def set_references(self, v):     self._set('references_data', v)
    def get_hobbies(self):           return self._get('hobbies_data')
    def set_hobbies(self, v):        self._set('hobbies_data', v)

    def to_dict(self):
        return {
            'id': self.pk, 'title': self.title, 'template': self.template,
            'full_name': self.full_name, 'email': self.email, 'phone': self.phone,
            'location': self.location, 'linkedin': self.linkedin, 'github': self.github,
            'website': self.website, 'twitter': self.twitter, 'summary': self.summary,
            'declaration_place': self.declaration_place,
            'declaration_date':  self.declaration_date,
            'photo_url': self.photo.url if self.photo else '',
            'education':        self.get_education(),
            'experience':       self.get_experience(),
            'skills':           self.get_skills(),
            'soft_skills':      self.get_soft_skills(),
            'projects':         self.get_projects(),
            'certifications':   self.get_certifications(),
            'languages':        self.get_languages(),
            'achievements':     self.get_achievements(),
            'courses':          self.get_courses(),
            'volunteer':        self.get_volunteer(),
            'extracurricular':  self.get_extracurricular(),
            'references':       self.get_references(),
            'hobbies':          self.get_hobbies(),
        }
