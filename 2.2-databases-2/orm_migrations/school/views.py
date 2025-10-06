from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Prefetch

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    students = Student.objects.prefetch_related(Prefetch('teachers', queryset=Teacher.objects.all(), to_attr='teacher_list'))
    context = {
        'object_list': students
    }

    return render(request, template, context)
