from django.db import models
from django.utils import timezone
import random

class Product(models.Model):
    CHAIR_TYPE_CHOICES = [
        ('lounge', 'Lounge Chair'),
        ('rocking', 'Rocking Chair'),
        ('recliner', 'Recliner Chair'),
        ('accent', 'Accent Chair'),
        ('patio', 'Patio Chair'),
        ('armchair', 'Armchair'),
        ('bar_stool', 'Bar Stool'),
        ('desk', 'Desk Chair'),
        ('outdoor', 'Outdoor Chair'),
        ('chaise_lounge', 'Chaise Lounge'),
        ('folding', 'Folding Chair'),
        ('deck', 'Deck Chair'),
        ('gaming', 'Gaming Chair'),
        ('bean_bag', 'Bean Bag Chair'),
        ('dining', 'Dining Chair'),
        ('wingback', 'Wingback Chair'),
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    has_rebate = models.BooleanField(default=False, null=True, blank=True)
    chair_type = models.CharField(max_length=50, choices=CHAIR_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else 'Unnamed Product'

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    # Existing fields
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True, default=0)  # Discount percentage
    has_rebate = models.BooleanField(default=False, null=True, blank=True)
    chair_type = models.CharField(max_length=50, null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    order_number = models.CharField(max_length=6, unique=True, editable=False)
    order_creation_date = models.DateTimeField(default=timezone.now)

    # New fields for payment and shipping details
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    card_exp = models.CharField(max_length=5, null=True, blank=True)  # MM/YY format
    cvv = models.CharField(max_length=3, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate final_price as price minus the discount
        if self.price and self.discount:
            self.final_price = self.price - (self.price * self.discount / 100)
        else:
            self.final_price = self.price  # If no discount, final_price equals price
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.name if self.name else 'Unnamed Product'}"
