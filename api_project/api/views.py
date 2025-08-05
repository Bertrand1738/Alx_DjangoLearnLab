from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


from django.http import JsonResponse

def book_list(request):
    data = {
        "books": [
            {"id": 1, "title": "Django for Beginners"},
            {"id": 2, "title": "Python Crash Course"}
        ]
    }
    return JsonResponse(data)

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Create your views here.
