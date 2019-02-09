from django.conf.urls import url

from .views import RegistrationAPIView

app_name = 'user'
urlpatterns = [
    url(r'^signup', RegistrationAPIView.as_view()),
]