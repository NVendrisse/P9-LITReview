from django.shortcuts import render, redirect
from django.db.models import Q
from . import forms, models
from authentification import models as auth


def personnal_feed(request):
        subscripted_user = models.UserFollows.objects.filter(user=request.user)
        subs_user = list(sub.followed_user for sub in subscripted_user)
        display_review = list(models.Review.objects.filter(Q(user=request.user) ^ Q(user__in=subs_user)))
        display_tickets = list(models.Ticket.objects.filter(Q(user=request.user) ^ Q(user__in=subs_user)))
        display_all = display_review + display_tickets
        display_all = sorted(display_all, key=lambda tc: tc.time_created,reverse=True)
        return render(request, "home.html", context={'feed':display_all})

def ticket_form(request):
    form = forms.NewTicketForm()
    if request.method == 'POST':
        form = forms.NewTicketForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.user = request.user
            save_form.save()
            return redirect('home')
    return render(request, "new_ticket.html", context={'form':form})

def review_form(request):
    form = forms.NewReviewForm()
    if request.method == 'POST':
        form = forms.NewReviewForm(request.POST)
        if form.is_valid():
            save = form.save(commit=False)
            save.user = request.user
            save.save()
            return redirect('home')
    return render(request, "new_review.html", context={'form':form})
    

def subscription(request):
    # faire un try à la place des ifs
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

    return render(request, "follow.html", context={'form':form, 'follows':follows})