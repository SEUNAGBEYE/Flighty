from django.conf.urls import url

from .views import TicketListCreate

app_name = 'ticket'
urlpatterns = [
    url(r'^$', TicketListCreate.as_view()),
]