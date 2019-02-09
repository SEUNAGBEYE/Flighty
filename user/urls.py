from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView

app_name = 'user'
urlpatterns = [
    url(r'^signup', RegistrationAPIView.as_view()),
    url(r'^signin', LoginAPIView.as_view()),
]