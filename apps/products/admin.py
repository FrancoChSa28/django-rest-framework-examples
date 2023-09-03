from django.contrib import admin
from .models import Customer, Product

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'updated_at', ]
    list_filter = ['email', ]
    search_fields = ['name']
    list_per_page = 50

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

