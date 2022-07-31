from django.urls import path

from display.views import DisplayView


urlpatterns = [
    path('image', DisplayView.as_view(), name='display'),
]
