from django.urls import path

from school.views import students_list

urlpatterns = [
    path('students/', students_list, name='students'),
]
