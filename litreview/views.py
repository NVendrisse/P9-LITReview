from django.shortcuts import render, redirect
from . import forms, models
from authentification import models as auth


class personnal_feed:
    
    def feed(request):
        subscripted_user = models.UserFollows.objects.all()
        tickets = models.Ticket.objects.all()
        return render(request, "home.html")

    def ticket_form(request):
        form = forms.NewTicketForm()
        if request.method == 'POST':
            form = forms.NewTicketForm(request.POST)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.user = request.user
                save_form.save()
                return redirect('home')
        return render(request, "home.html", context={'form':form})
    

def subscription(request):
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