from django.db import models

# Create your models here.
from django.db import models

class Car(models.Model):
    username = models.CharField(max_length=400, default="Hubli")
    car_name = models.CharField(max_length=100)
    status = models.CharField(max_length=400, default="Active")
    extracted_data = models.CharField(max_length=400, default="Hubli")
    number_plate = models.CharField(max_length=15)
    entered_timings = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='car_images/',default='img')  # Specify the directory where images will be uploaded


class CarLogin(models.Model):
    username = models.CharField(max_length=400, default="Hubli")
    number_plate = models.CharField(max_length=15)
    entered_timings = models.CharField(max_length=15,default='0')
    entered_timings1 = models.DateTimeField(auto_now_add=True)

