from django.urls import path

from display.views import DisplayView


urlpatterns = [
    path('image/<int:id>', DisplayView.as_view(), name='team'),
]
