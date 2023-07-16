from django.http import HttpResponse
from django.shortcuts import render


def user_page(requested_user):
    return HttpResponse('<h1> USER PAGE </h1>')
