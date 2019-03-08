from django.db import models

class Subscriber(models.Model):
    subscriber = models.EmailField()

    def __str__(self):
        return self.subscriber
