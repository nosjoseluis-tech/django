from django.urls import path

from .views import (
    AuthorListCreateView,
    AuthorDetailView,
    BookDetailView,
    BookListCreateView,
    CategoryDetailView,
    CategoryListCreateView,
    LoanDetailView,
    LoanListCreateView,
    AuthorStatsView,
    BookStatsView,
    BookSearchView,
    BookIncreaseStockView,
    BookFilterView
)

urlpatterns = [
    path("authors/", AuthorListCreateView.as_view(), name="author-list-create"),
    path("authors/stats/", AuthorStatsView.as_view(), name="author-stats"),
    path("authors/<int:author_id>/", AuthorDetailView.as_view(), name="author-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:category_id>/", CategoryDetailView.as_view(), name="category-detail"),
    path("books/search/", BookSearchView.as_view(), name="book-search"),
    path("books/stats/", BookStatsView.as_view(), name="book-stats"),
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:book_id>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:book_id>/increase-stock", BookIncreaseStockView.as_view(), name="book-increase-stock"),
    path("books/filter/", BookFilterView.as_view(), name="book-filter"),
    path("loans/", LoanListCreateView.as_view(), name="loan-list-create"),
    path("loans/<int:loan_id>/", LoanDetailView.as_view(), name="loan-detail")
]