from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
class BookViewSet(viewsets.ModelViewSet):
    """
    This API uses token authentication. Obtain a token at /api/token/ by POSTing your username and password.
    All endpoints require a valid token in the `Authorization` header.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
