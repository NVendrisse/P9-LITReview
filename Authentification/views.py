from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.conf import settings
from . import forms

def login_page(requested_user):
    form = forms.LoginForm()
    if requested_user.method == 'POST':
        form = forms.LoginForm(requested_user.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'],)
        if user is not None:
            login(requested_user, user)
            return redirect('home')
    return render(requested_user,'login.html', context={'form': form})

def create_user(new_user):
    form = forms.CreateNewAccount()
    if new_user.method == 'POST':
        form = forms.CreateNewAccount(new_user.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    return render(new_user,'new_account.html', context={'form': form})