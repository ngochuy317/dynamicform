from .views import *
from django.urls import path, include


urlpatterns = [
    path('forms/', ListFormDataView.as_view(), name='list_forms'),
    path('forms/<slug:slug>', RetrieveFormData.as_view(), name='retrieve_forms'),

    path('provinces/', ListProvincesView.as_view(), name='provinces'),
    path('create-provinces/', CreateProvincesView.as_view(),
         name='create_provinces'),
]
