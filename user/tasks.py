import os
from django.conf import settings
from flighty.celery import app

@app.task(name='delete_passport_image')
def delete_passport_image(image_path):
    """
    Deletes passport image
    """
    try:
        os.remove(image_path)
    except FileNotFoundError:
        print('File not found')