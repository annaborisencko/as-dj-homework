from django.db import models
from datetime import datetime

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    description = models.CharField(max_length=250, null=True, verbose_name='Описание')

    def __str__(self):
        return f'Датчик {self.id} "{self.name}"'
    
class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='Датчик', related_name='measurements')
    temperature = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Температура')
    date_of_measure = models.DateTimeField(auto_now=True, verbose_name='Дата и время измерения')
    image = models.ImageField(null=True, verbose_name='Изображение с измерением')
    def __str__(self):
        return f'{self.date_of_measure} - {self.sensor.id} - {self.temperature}C'
    