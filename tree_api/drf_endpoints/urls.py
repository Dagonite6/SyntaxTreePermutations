from django.urls import path
from . import views

urlpatterns = [
    path('', views.NP_phrase.as_view(), name='np-phrase'),
]