from django.conf.urls import url

from .views import TicketListCreate, TicketRetrieveUpdateDestroyAPIView

app_name = 'ticket'
urlpatterns = [
    url(r'^$', TicketListCreate.as_view()),
     url(r'^(?P<id>\d+)$', TicketRetrieveUpdateDestroyAPIView.as_view()),
]