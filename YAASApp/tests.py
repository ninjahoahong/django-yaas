from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from YAASApp.models import Auction
from YAASApp.views import register

__author__ = 'Duong Duc Anh'

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def testUC3(self):
        client = Client()
        response = client.get('/addauction/')
        response.status_code
        self.client.login(username='anh', password='anh')
        response = client.get('/addauction/') # get response from /addauction/
        response.status_code

    def testUC6(self):
        client = Client()
        auction = Auction()
        response = client.get('/addbid/'+auction.id)
        response.status_code
        self.client.login(username='anh', password='anh')
        response = client.get('/addbid/'+auction.id)
        response.status_code

    def testUC10(self):
        pass


