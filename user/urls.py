from django.conf.urls import url

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'user'
urlpatterns = [
    url(r'^signup', RegistrationAPIView.as_view(), name='signup'),
    url(r'^signin', LoginAPIView.as_view(), name='signin'),
    url(r'^profile', UserRetrieveUpdateAPIView.as_view(), name='profile'),
]