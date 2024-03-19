from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.staticfiles import finders
from requests import Request

Class test_page(TestCase):



def get_request():
    request=Request()
    page_id=None
    if request.method=='GET':
        if 'page_id' in request.GET:
            page_id=request.GET['page_id']
            print("test_page class's page_id:",page_id)