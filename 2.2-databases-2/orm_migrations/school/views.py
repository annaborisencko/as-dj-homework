from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    students = Student.objects.all()
    context = {
        'object_list': students
    }

    return render(request, template, context)
