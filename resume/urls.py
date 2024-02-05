from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    path('build',home,name='build'),
    path('build/personaldetails',personal_details.as_view(),name='build/personal_details'),
    path('build/education_details', education_details.as_view(), name='build/education_details'),
    path('build/internship_details',internship_details.as_view(),name='build/internship_details'),
    path('build/project_details', project_details.as_view(), name='build/project_details'),
    path('build/skills',skills.as_view(),name="build/skills"),
    path('build/languages_details', languages.as_view(), name="build/languages_details"),
    path('build/achievements_details', achievements_details.as_view(), name="build/achievements_details"),
    path('build/showtemplates',showtemplates,name='build/showtemplates'),
    path('select-resume',resume1,name='resume1'),
    path('select-resume2',resume2,name='resume2'),
    path('del',dele),
]
