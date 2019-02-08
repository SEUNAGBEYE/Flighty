from django.conf.urls import url

from .views import TicketListCreate, TicketRetrieveUpdateDestroyAPIView

app_name = 'ticket'
urlpatterns = [
    url(r'^(?P<id>\d+)$', TicketRetrieveUpdateDestroyAPIView.as_view()),
    url(r'^$', TicketListCreate.as_view()),
]