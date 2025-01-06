from django.db import models

class Data(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField(null=True)

    def __str__(self):
        return f"Message at {self.timestamp}"
