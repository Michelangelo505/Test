from django.urls import path
from .views import *

app_name = 'tradegems'

urlpatterns = [
    path('customers/',CustomerView.as_view()),
]
