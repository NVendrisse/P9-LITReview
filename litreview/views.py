from django.shortcuts import render, redirect
from django.db.models import Q
from django.db import IntegrityError
from . import forms, models
from authentification import models as auth
from django.core.exceptions import ObjectDoesNotExist


def personnal_feed(request):
        subscripted_user = models.UserFollows.objects.filter(user=request.user)
        subs_user = list(sub.followed_user for sub in subscripted_user)
        display_review = list(models.Review.objects.filter(Q(user=request.user) | Q(user__in=subs_user)))
        display_tickets = list(models.Ticket.objects.filter(Q(user=request.user) | Q(user__in=subs_user)))
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
    to_subs = auth.User()
    subscripted = models.UserFollows.objects.filter(user=request.user)
    follows = models.UserFollows.objects.filter(followed_user=request.user)
    to_subs_userfollows = models.UserFollows()
    error_message = ''
    if request.method == 'POST':
        try:
            to_subs = auth.User.objects.get(username=request.POST.get('searchbar'))
            to_subs_userfollows = models.UserFollows(user=request.user,followed_user=to_subs)
            to_subs_userfollows.save()

        except request.user == to_subs:
            error_message = "Vous ne pouvez pas vous abonner a vous même"
        
        except to_subs.DoesNotExist:      
            error_message = "Cet utilisateur n'existe pas"
            
        except IntegrityError:
            error_message = "Vous ne pouver pas vous abonner à {}".format(to_subs)

    return render(request, "follow.html", context={'subscripted':subscripted,'follows':follows, 'error':error_message})

def unsuscribe(request, id):
    print(id)
    unfollow = models.UserFollows.objects.get(id=id)
    if request.method == 'POST':
        unfollow.delete()
        return redirect('subscription')