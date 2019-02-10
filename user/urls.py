from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'user'
urlpatterns = [
    url(r'^signup', RegistrationAPIView.as_view()),
    url(r'^signin', LoginAPIView.as_view()),
    url(r'^profile', UserRetrieveUpdateAPIView.as_view()),
]