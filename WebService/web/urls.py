from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('forms', FormTitleView.as_view()),
    path('user', UserView.as_view()),
    path('user/<str:username>', FormOfUserView.as_view()),
    path('user/<str:username>/<slug:slug>', DetailFormOfUserView.as_view()),
    # path('save_formdata/<int:pk>', RetrieveUpdateDestroyData.as_view()),
]
