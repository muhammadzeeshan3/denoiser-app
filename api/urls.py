from django.urls import path
from api.views import *

urlpatterns = [
    path('denoiser/', DenoiserAPIView.as_view(), name='Denoiser'),

]