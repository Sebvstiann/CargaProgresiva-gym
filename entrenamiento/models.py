from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return self.username

class Rutina(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=255)
    es_cardio = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class RegistroEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)

    series = models.IntegerField(null=True, blank=True)
    peso_agregado_KG = models.FloatField(null=True, blank=True)
    
    repeticiones_en_la_primera_serie = models.IntegerField(null=True, blank=True)
    repeticiones_en_la_segunda_serie = models.IntegerField(null=True, blank=True)
    repeticiones_en_la_tercera_serie = models.IntegerField(null=True, blank=True)

    observaciones = models.TextField(null=True, blank=True)
    rendimiento_percibido = models.IntegerField(null=True, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.ejercicio.nombre} ({self.fecha_hora.date()})"
