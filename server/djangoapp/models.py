from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):  # CarMake is defined FIRST
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name

class CarModel(models.Model):  # THEN CarModel can use CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    name = models.CharField(max_length=100)
    
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    
    dealer_id = models.IntegerField()
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2025),
            MinValueValidator(2015)
        ])
    
    def __str__(self):
        return f"{self.car_make.name} {self.name}"
