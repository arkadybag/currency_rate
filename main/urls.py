from django.urls import path

from main import views

urlpatterns = [
    path('currencies', views.CurrencyView.as_view()),
    path('rate/<currency>/', views.RateView.as_view()),
]
