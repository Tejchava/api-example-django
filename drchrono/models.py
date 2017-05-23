from django.db import models

# Create your models here.

# With this Model Structure we are going to store scheduled birthday details.

class PatientDetails(models.Model):
    def __str__(self):
        return self.email + " " + str(self.userId)

    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=1000)
    dob = models.CharField(max_length=10)
    userId = models.BigIntegerField(primary_key=True)
    greeting = models.CharField(max_length=10000)