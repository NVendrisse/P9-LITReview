from django.shortcuts import render


def personnal_feed(user):
    return render(user, "home.html")
