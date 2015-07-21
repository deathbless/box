from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bank(models.Model):
    card_number = models.CharField(max_length=20)
    balance = models.FloatField()

    def __unicode__(self):
        return self.card_number

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    idcard = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    cards = models.ManyToManyField(Bank)

class Item(models.Model):
    publisher = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    pic = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    catalog = models.CharField(max_length=50)

class Order(models.Model):
    buyer = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    order_time = models.DateTimeField()
    is_set = models.BooleanField()
    is_buy = models.BooleanField()
    is_complete = models.BooleanField()
    box_id = models.IntegerField()
    comment = models.TextField()