from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
class categorydb(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    details = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
