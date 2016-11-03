from django.db import models
import uuid


class App(models.Model):
    token_id = models.CharField(max_length=128, default=uuid.uuid4, blank=False, unique=True)
    name = models.CharField(max_length=128, default="Sandbox", blank=False)
