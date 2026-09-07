from django.contrib import admin

from .models import (
    Book,
    Author,
    Category,
    Loan
)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    @admin.display(description="Categorires")
    def categoriesList(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    
    list_display = ("title", "price", "stock", "author", "categoriesList", "is_available", "created_at", )

    search_fields = ("title", "author__name", )

    list_filter = ("is_available", "author", )

    ordering = ("-created_at", )

    fieldsets = (
        (
            "Information", 
            {
                "fields": (
                    "title",
                    "author",
                    "categories",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                    "is_available",
                )
            },
        ),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_year", )

    search_fields = ("name", )

    list_filter = ("name", )

    ordering = ("-birth_year", )

    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "name",
                    "birth_year",
                )
            },
        ),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

    search_fields = ("name", )

    list_filter = ("name", )

    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "name",
                )
            },
        ),
    )

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user_name", "book", "quantity", "status", "created_at", )

    search_fields = ("user_name", "book__title", )

    list_filter = ("user_name", "status", )

    ordering = ("-created_at", )

    fieldsets = (
        (
            "Information", 
            {
                "fields": (
                    "user_name",
                    "book",
                    "quantity",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                )
            },
        ),
    )