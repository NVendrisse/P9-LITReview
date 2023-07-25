from django.shortcuts import render, redirect
from . import forms


def personnal_feed(user):
    return render(user, "home.html")

def subscription(request):
    form = forms.SocialForm(instance=request.user)
    if request.method == 'POST':
        form = forms.SocialForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "follow.html", context={'form':form})