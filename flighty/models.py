from django.db import models


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']
    
    @classmethod
    def get_or_404(cls, id):
        response = {}
        status_code = 200
        try:
            response = cls.objects.get(pk=id)
        except cls.DoesNotExist:
            response = {
                'errors': {
                    'id': [f'{cls.__name__} does not exist']
                }
            }
            status_code = 404
        return response, status_code