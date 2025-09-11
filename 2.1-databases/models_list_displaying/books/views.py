from django.shortcuts import render
from .models import Book
from datetime import datetime


def books_view(request):
    template = 'books/books_list.html'
    book_list = Book.objects.all()
    context = {
        'book_list': book_list
    }
    return render(request, template, context)

def books_by_date_view(request, get_date):
    template = 'books/books_list.html'
    msg = ''
    get_date = datetime.date(get_date)
    pub_date_list = Book.objects.values_list('pub_date', flat=True)
    if get_date not in list(pub_date_list):
        msg = f"В каталоге отсутствуют книги с указанной Вами датой выпуска {get_date.strftime("%Y-%m-%d")}"
    
    next_date = Book.objects.filter(pub_date__gt=get_date).order_by('pub_date')
    if next_date:
        next_date = next_date[0].pub_date
    else:
        next_date = None

    previous_date = Book.objects.filter(pub_date__lt=get_date).order_by('-pub_date')
    if previous_date:
        previous_date = previous_date[0].pub_date
    else:
        previous_date = None

    book_list = Book.objects.filter(pub_date=get_date)
    
    context = {
        'get_date': get_date,
        'book_list': book_list,
        'next_date': next_date,
        'previous_date': previous_date,
        'msg': msg,
    }
    return render(request, template, context)