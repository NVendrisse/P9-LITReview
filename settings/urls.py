"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentification import views as auth_view
from litreview import views as main_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_view.login_page, name="login"),
    path("logout/", auth_view.log_out, name="logout"),
    path("new_account/", auth_view.create_user, name="signup"),
    path("home/", main_views.personnal_feed, name="home"),
    path("newticket/", main_views.ticket_form, name="ticket"),
    path("newticket/<int:ticket_id>/", main_views.ticket_form, name="ticket"),
    path("newreview/<int:ticket_id>/", main_views.review_form, name="review"),
    path(
        "newreview/<int:ticket_id>/<int:review_id>/",
        main_views.review_form,
        name="review",
    ),
    path("newreview/", main_views.review_form, name="review"),
    path("subscription/", main_views.subscription, name="subscription"),
    path("unsuscribe/<int:id>/", main_views.unsuscribe, name="unsuscribe"),
    path("delete/<str:type>/<int:id>/", main_views.delete_post, name="delete"),
    path("myposts/", main_views.my_posts, name="myposts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
