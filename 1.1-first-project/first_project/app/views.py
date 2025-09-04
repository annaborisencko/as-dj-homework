from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
import os
from first_project.settings import BASE_DIR

def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
    return render(request, 'app/current_time.html', {'current_time': current_time})
    # msg = f'Текущее время: {current_time}'
    # return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    workdir_file_list = os.listdir(BASE_DIR+'/app')
    # raise NotImplemented
    return render(request, 'app/workdir_file_list.html', {'workdir_file_list': workdir_file_list})
