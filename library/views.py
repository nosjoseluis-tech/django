from django.db.models import Avg, Q, F, Count, Sum
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView

from .models import (
    Author,
    Category,
    Book,
    Loan
)

from .serializers import (
    AuthorSerializer,
    BookSerializer,
    CategorySerializer,
    LoanSerializer
)

class AuthorListCreateView(APIView):
    def get(self, request):
        authors = Author.objects.all()

        serializer = AuthorSerializer(authors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AuthorDetailView(APIView):
    def put(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AuthorSerializer(author, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        author.delete()

        return Response(
            {"message": "Author deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AuthorSerializer(author)

        return Response(serializer.data)

class AuthorStatsView(APIView):
    def get(self, request):
        authors = Author.objects.annotate(book_count=Count("books"))

        data = [
            {"id": author.id, "name": author.name, "book_count": author.book_count}
            for author in authors
        ]

        return Response(data)

class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryDetailView(APIView):
    def put(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()

        return Response(
            {"message": "Category deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category)

        return Response(serializer.data)

class BookListCreateView(APIView):
    def get(self, request):
        books = Book.objects.select_related("author").prefetch_related("categories")

        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class BookDetailView(APIView):
    def put(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        book.delete()

        return Response(
            {"message": "Book deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(book)

        return Response(serializer.data)

class BookSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        books = Book.objects.filter(title__icontains=query).select_related("author").prefetch_related("categories")
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

class BookFilterView(APIView):
    def get(self, request):
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        filters = Q()

        if min_price:
            filters &= Q(price__gte=min_price)

        if max_price:
            filters &= Q(price__lte=max_price)

        books = Book.objects.filter(filters).select_related("author").prefetch_related("categories")

        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

class BookIncreaseStockView(APIView):
    def post(self, request, book_id):
        try:
            quantity = int(request.data.get("quantity"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not quantity or int(quantity) <= 0:
            return Response(
                {"error": "The amount must be positive"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        book.stock = F("stock") + int(quantity)
        book.save()
        book.refresh_from_db()

        serializer = BookSerializer(book)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class BookStatsView(APIView):
    def get(self, request):
        stats = Book.objects.aggregate(
            total_books=Count("id"),
            average_price=Avg("price"),
            total_stock=Sum("stock")
        )

        return Response(stats)

class LoanListCreateView(APIView):
    def get(self, request):
        loans = Loan.objects.select_related("book", "book__author").prefetch_related("book__categories")

        serializer = LoanSerializer(loans, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = LoanSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class LoanDetailView(APIView):
    def put(self, request, loan_id):
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LoanSerializer(loan, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, loan_id):
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        loan.delete()

        return Response(
            {"message": "Loan deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LoanSerializer(loan)

        return Response(serializer.data)