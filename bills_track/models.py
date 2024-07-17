from django.db import models

# Create your models here.
class Bill(models.Model):
    name_of_item = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)