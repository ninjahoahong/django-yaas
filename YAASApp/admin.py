__author__ = 'Duong Duc Anh'

from django.contrib import admin
from YAASApp.models import Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('seller', 'title', 'end_time', 'state')
    search_fields = ['title']

admin.site.register(Auction, AuctionAdmin)