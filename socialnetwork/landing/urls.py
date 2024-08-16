from django.urls import path
from landing.views import *


urlpatterns = [
    path('',Index.as_view(),name='index')
]
