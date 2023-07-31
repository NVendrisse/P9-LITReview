from django.shortcuts import render, redirect
from . import forms, models
from authentification import models as auth

def personnal_feed(user):
    return render(user, "home.html")

def subscription(request):
    #la
    form = forms.SocialForm()
    all_users = auth.User.objects.all()
    follows = models.UserFollows.objects.all()
    if request.method == 'POST':
        form = forms.SocialForm(request.POST)
        if form.is_valid():
            subscription_list = list(follows)
            save_form = form.save(commit=False)
            user_subs_list = list()
            for subs in subscription_list:
                couple = (subs.user, subs.followed_user)
                user_subs_list.append(couple)
            new_subscription = (request.user, save_form.followed_user)
            if new_subscription not in user_subs_list:
                if request.user != save_form.followed_user:
                    save_form.user = request.user
                    save_form.save()

    return render(request, "follow.html", context={'form':form, 'users':all_users, 'follows':follows})