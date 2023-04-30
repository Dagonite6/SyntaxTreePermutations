from django.urls import path
from . import views

urlpatterns = [
    path('', views.NP_paraphrase.as_view(), name='np-phrase'),
    path('testing/', views.testing_view.as_view(), name='api-testing')
]