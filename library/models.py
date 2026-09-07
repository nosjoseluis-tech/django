from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=40)
    birth_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(
        Category
    )
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Loan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        RETURNED = "returned", "Returned"

    user_name = models.CharField(max_length=40)
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} to {self.user_name}"