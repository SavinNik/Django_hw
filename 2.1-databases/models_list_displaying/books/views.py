from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Min, Max
from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


def date_book_view(request, select_date):
    try:
        select_date = datetime.strptime(select_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('books')

    books = Book.objects.filter(pub_date=select_date)
    if books.exists():
        prev_date_result = Book.objects.filter(pub_date__lt=select_date).aggregate(Min('pub_date'))
        prev_date = prev_date_result['pub_date__min']

        next_date_result = Book.objects.filter(pub_date__gt=select_date).aggregate(Min('pub_date'))
        next_date = next_date_result['pub_date__min']

        template = 'books/date_book.html'
        context = {"books": books,
                   "prev_date": prev_date,
                   "next_date": next_date,
                   }
        return render(request, template, context)
    else:
        return redirect('books')
