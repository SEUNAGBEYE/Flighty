from flighty.celery import app
from flighty.send_email import email
from .models import Ticket
from datetime import datetime, timedelta
from .serializers import TicketSerializer


@app.task(name='send_e_tickets')
def send_e_ticket(instance, recipient, subject, body=None):
    """
    Sends e tickets to users.
    """
    flight = instance.pop('flight')
    passengers = instance.pop('passengers')
    if instance:
        email(subject,
            [recipient],
            'e_ticket.html',
            context={
                'flight': flight,
                'passengers': passengers,
                'ticket': instance,
                'body': body
            }
        )

@app.task(name='send_travel_notification')
def send_travel_notification():
    """
    Reminds users that their flight is tomorrow
    """
    departure_date = (datetime.now() + timedelta(hours=24)).date()
    #using a startswith lookup because __date lookup is not supported by django. Moreover, date are just strings. 2017-07-11 will match 2017-07-11:06:00+01:00
    tickets = Ticket.objects.filter(flight__departure_date__startswith=str(departure_date),
    is_ticketed=True, is_valid=True
    ).all() # We don't want to send reminders to users that have not purchased their tickets (booking only) so we add is_ticketed to the query.
    tickets_data = TicketSerializer(tickets, many=True).data
    body = 'Your flight tomorrow'
    for ticket in tickets_data:
        send_e_ticket.delay(ticket, ticket['user']['email'], 'Travel Reminder!', body)