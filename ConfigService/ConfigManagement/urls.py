from django.urls import path
from .views import ListConfigView, RetrieveConfigView

urlpatterns = [
    path('',ListConfigView.as_view()),
    path('<str:key>/',RetrieveConfigView.as_view()),
    path('<str:key>/<str:version>/',RetrieveConfigView.as_view()),
]