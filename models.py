from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Bank(models.Model):
    card_number = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    balance = models.FloatField()

    def __unicode__(self):
        return self.card_number


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    idcard = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    cards = models.OneToOneField(Bank)
    nfc = models.CharField(max_length=20)

    def as_json(self):
        return dict(
            username=self.user.username,
            name=self.user.first_name,
            email=self.user.email,
            idcard=self.idcard,
            phone=self.phone,
            bankcard=self.cards.card_number,
            nfc = self.nfc
        )

    def __unicode__(self):
        return self.user.username + '\'s Profile'


class Item(models.Model):
    publisher = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    pic = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    catalog = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.id) + ' ' + self.title

    def as_json(self):
        return dict(
            item_id = self.id,
            seller=self.publisher.username,
            title=self.title,
            pic=self.pic,
            description=self.description,
            quantity=self.quantity,
            price=self.price.to_eng_string(),
            start_time=self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time=self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            catalog=self.catalog
        )


class Order(models.Model):
    buyer = models.ForeignKey(User)
    seller = models.CharField(max_length=50)
    item = models.ForeignKey(Item)
    order_time = models.DateTimeField()
    is_set = models.BooleanField()
    is_paid = models.BooleanField()
    is_complete = models.BooleanField()
    box_id = models.IntegerField(blank=True)
    comment = models.TextField(blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.id) + ' ' + self.buyer.username + ' ' + self.item.title

    def as_json(self):
        return dict(
            order_id=self.id,
            buyer=self.buyer.username,
            seller=self.seller,
            item_id=self.item.id,
            item_name=self.item.title,
            order_time=self.order_time.strftime('%Y-%m-%d %H:%M:%S'),
            quantity=self.quantity,
            price=self.price.to_eng_string(),
            is_set=self.is_set,
            is_paid=self.is_paid,
            is_complete=self.is_complete,
            comment=self.comment
        )
