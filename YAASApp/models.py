from django.core.mail import send_mail

__author__ = 'Duong Duc Anh'

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#class Receipt(models.Model):
#    seller = models.ForeignKey(User)
#    bids = models.ManyToManyField(Bid, null=True, blank=True)

AUCTION_STATES = (
    ('A', 'Active'),
    ('B', 'Banned'),
    ('D', 'Due'),
    ('J', 'Adjudicated'),
)

class Auction(models.Model):
    #receipts = models.ManyToManyField(Receipt, blank=True)
    seller = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description = models.TextField()
    min_price = models.DecimalField(max_digits=10 ,decimal_places=2)
    end_time = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=1, choices=AUCTION_STATES)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    @classmethod
    def getByName (cls, auction_name):
        return cls.objects.get(title = auction_name)

    @classmethod
    def getByID (cls, auction_id):
        return cls.objects.get(id = auction_id)

    def save(self):
        if self.state == 'B':
            bidders = [b.bidder.email for b in Bid.objects.filter(auction_id = self.id)]
            send_mail('No-reply: Auction Banned', 'Your auction has been banned by admin', 'admin@example.com',
                      [self.seller.email]+bidders, fail_silently=False)
        super(Auction, self).save()

class Bid(models.Model):
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(Auction)
    bidder = models.ForeignKey(User)
