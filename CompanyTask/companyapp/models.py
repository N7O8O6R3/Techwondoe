
# Create your models here.
import uuid
from django.db import models

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    companyName = models.CharField(max_length=100)
    companyCEO = models.CharField(max_length=100)
    companyAddress = models.TextField(max_length=300)
    inceptionDate = models.DateField()


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    companyID = models.ForeignKey(Company, on_delete=models.CASCADE)
    teamLeadName = models.CharField(max_length=100)