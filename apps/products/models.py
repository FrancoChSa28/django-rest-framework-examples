from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=200,
        db_column='name'
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        db_column='email'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_column='updated_at'
    )

    def __str__(self):
        return 'Name: {0}, Email: {1}'.format(self.name, self.email)

    class Meta:
        db_table = 'tbl_customers'
        ordering = ['id']

class Product(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column='customer_id'
    )
    product_id = models.CharField(
        max_length=200,
        db_column='product_id'
    )
    product_title = models.CharField(
        max_length=200,
        db_column='product_title'
    )
    product_price = models.FloatField(db_column='product_price')
    product_image = models.URLField(
        max_length=200,
        db_column='product_image'
    )
    review_score = models.FloatField(
        null=True,
        default=None,
        db_column='review_score'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_column='updated_at'
    )

    def __str__(self):
        return 'Customer: {0}, ProductID: {1}'.format(self.customer, self.product_id)

    class Meta:
        db_table = 'tbl_customer_products'
        ordering = ['id']
        unique_together = [
            ['customer', 'product_id'],
        ]
