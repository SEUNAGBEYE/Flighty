from django.conf.urls import url

from .views import TicketListCreate, TicketRetrieveUpdateDestroyAPIView

app_name = 'ticket'
urlpatterns = [
    url(r'^$', TicketListCreate.as_view(), name='ticket-create-list'),
     url(r'^(?P<id>\d+)$', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-retrieve-update'),
]