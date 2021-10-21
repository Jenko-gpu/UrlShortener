
from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect),
    path('shorten', views.create),
    path('<str:shortenedUrl>', views.redirect),
    path('<str:shortenedUrl>/views', views.show_views)
]