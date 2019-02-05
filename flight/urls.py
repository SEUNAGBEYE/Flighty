from django.urls import path


app_name = 'user'
urlpatterns = [
    path('status', lambda x: x),
    path('destinations', lambda x: x),
]