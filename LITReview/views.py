from django.http import HttpResponse
from django.shortcuts import render


def login_page(requested_user):
    return render(requested_user,'login.html')

def create_user(new_user):
    return render(new_user,'new_account.html')
