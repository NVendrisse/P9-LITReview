from django.shortcuts import render, redirect
from django.db.models import Q
from django.db import IntegrityError
from . import forms, models
from authentification import models as auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


@login_required
def personnal_feed(request):
    subscripted_user = models.UserFollows.objects.filter(user=request.user)
    subs_user = list(sub.followed_user for sub in subscripted_user)
    display_review = list(
        models.Review.objects.filter(Q(user=request.user) | Q(user__in=subs_user))
    )
    display_tickets = list(
        models.Ticket.objects.filter(Q(user=request.user) | Q(user__in=subs_user))
    )
    display_all = display_review + display_tickets
    display_all = sorted(display_all, key=lambda tc: tc.time_created, reverse=True)
    return render(request, "home.html", context={"feed": display_all})


@login_required
def my_posts(request):
    display_myreview = list(models.Review.objects.filter(user=request.user))
    display_mytickets = list(models.Ticket.objects.filter(user=request.user))
    display_mypost = display_myreview + display_mytickets
    display_mypost = sorted(
        display_mypost, key=lambda tc: tc.time_created, reverse=True
    )
    return render(request, "myposts.html", context={"feed": display_mypost})


@login_required
def ticket_form(request, ticket_id: int = None):
    if not ticket_id == None:
        existing_ticket = models.Ticket.objects.get(id=ticket_id)
        if request.user == existing_ticket.user:
            form = forms.NewTicketForm(instance=existing_ticket)
        else:
            return redirect("home")
    else:
        existing_ticket = None
        form = forms.NewTicketForm()

    if request.method == "POST":
        form = forms.NewTicketForm(
            request.POST, request.FILES, instance=existing_ticket
        )
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.user = request.user
            save_form.save()
            return redirect("home")

    return render(request, "new_ticket.html", context={"form": form})


@login_required
def review_form(request, ticket_id: int = None, review_id: int = None):
    form = forms.NewReviewForm()
    if not ticket_id == None:
        ticket_item = models.Ticket.objects.get(id=ticket_id)
        t_form = forms.NewTicketForm(instance=ticket_item)
        if not request.user == ticket_item.user:
            for field in t_form.fields:
                t_form.fields[field].widget.attrs["readonly"] = True
    else:
        t_form = forms.NewTicketForm()
    if not review_id == None:
        review_item = models.Review.objects.get(id=review_id)
        form = forms.NewReviewForm(instance=review_item)
    else:
        review_item = None
        form = forms.NewTicketForm()
    if request.method == "POST":
        if ticket_id == None:
            t_form = forms.NewTicketForm(request.POST)
            if t_form.is_valid():
                t_save = t_form.save(commit=False)
                t_save.user = request.user
                t_save.save()
                ticket_id = t_save.id

        form = forms.NewReviewForm(request.POST, instance=review_item)
        if form.is_valid():
            save = form.save(commit=False)
            save.ticket_id = ticket_id
            save.user = request.user
            save.save()
            return redirect("home")
    return render(request, "new_review.html", context={"form": form, "ticket": t_form})


@login_required
def subscription(request):
    to_subs = auth.User()
    subscripted = models.UserFollows.objects.filter(user=request.user)
    follows = models.UserFollows.objects.filter(followed_user=request.user)
    to_subs_userfollows = models.UserFollows()
    error_message = ""
    if request.method == "POST":
        try:
            to_subs = auth.User.objects.get(username=request.POST.get("searchbar"))
            if not to_subs == request.user:
                to_subs_userfollows = models.UserFollows(
                    user=request.user, followed_user=to_subs
                )
                to_subs_userfollows.save()
            else:
                raise IntegrityError

        except to_subs.DoesNotExist:
            error_message = "Cet utilisateur n'existe pas"

        except IntegrityError:
            error_message = "Vous ne pouver pas vous abonner à {}".format(to_subs)

    return render(
        request,
        "follow.html",
        context={
            "subscripted": subscripted,
            "users": to_subs,
            "follows": follows,
            "error": error_message,
        },
    )


@login_required
def unsuscribe(request, id):
    unfollow = models.UserFollows.objects.get(followed_user_id=id, user=request.user)
    if request.method == "POST":
        unfollow.delete()
        return redirect("subscription")


@login_required
def delete_post(request, type, id):
    if type == "ticket":
        delete = models.Ticket.objects.get(id=id)
    elif type == "review":
        delete = models.Review.objects.get(id=id)
    if request.method == "POST":
        delete.delete()
    return redirect("myposts")
