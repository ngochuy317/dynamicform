from django.urls import path

from . import views


app_name = 'data'
urlpatterns = [
   path('api/forms', views.FormTitleView.as_view()),
   path('api/user', views.UserView.as_view()),
   path('api/user/<str:username>', views.FormOfUserView.as_view()),
   path('api/user/<str:username>/<slug:slug>', views.DetailFormOfUserView.as_view()),
   path('api/save_formdata/', views.DataView.as_view()),
   path('api/save_formdata/<int:pk>', views.RetrieveUpdateDestroyData.as_view()),
]