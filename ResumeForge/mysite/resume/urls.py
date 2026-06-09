from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/new/', views.create_resume, name='create_resume'),
    path('resume/<int:pk>/build/', views.build_resume, name='build_resume'),
    path('resume/<int:pk>/preview/', views.preview_resume, name='preview_resume'),
    path('resume/<int:pk>/save/', views.save_resume, name='save_resume'),
    path('resume/<int:pk>/upload-photo/', views.upload_photo, name='upload_photo'),
    path('resume/<int:pk>/duplicate/', views.duplicate_resume, name='duplicate_resume'),
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:pk>/download/', views.download_pdf, name='download_pdf'),
]
