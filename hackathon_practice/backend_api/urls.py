from django.urls import path
from .views import *
from .test import test_view  # note the function, not the module

urlpatterns = [
    path('generate/', generate_text, name='generate_text'),
    path('test/', test_view, name='test'),
    path('question/', generate_questions, name='generate_questions'),
    path('check/', check_answers, name = 'check_answers')
]
