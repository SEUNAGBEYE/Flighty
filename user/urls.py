from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'user'
urlpatterns = [
    path('signup', RegistrationAPIView.as_view()),
    path('signin', LoginAPIView.as_view()),
    path('profile', UserRetrieveUpdateAPIView.as_view()),
]