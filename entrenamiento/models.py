from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class Usuario(AbstractUser):
    peso = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0, message="El peso debe ser un número positivo")]
    )
    altura = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0, message="La altura debe ser un número positivo")]
    )
    edad = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0, message="La edad debe ser un número positivo")]
    )
    imagen = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def perfil_completo(self):
        return all([self.peso, self.altura, self.edad])

    def __str__(self):
        return self.username

class Rutina(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='ejercicios',
        null=True,
        blank=True
    )
    imagen = models.ImageField(
        upload_to='ejercicios/',
        null=True,
        blank=True,
        help_text='Imagen de referencia del ejercicio'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción y técnica del ejercicio'
    )

    def __str__(self):
        return f"{self.nombre} - {self.rutina.nombre if self.rutina else 'Sin rutina'}"

    class Meta:
        ordering = ['rutina', 'nombre']

class RegistroEntrenamiento(models.Model):
    RENDIMIENTO_CHOICES = [
        (1, '😫 Muy Malo'),
        (2, '😞 Malo'),
        (3, '😐 Regular'),
        (4, '😊 Bueno'),
        (5, '🤩 Excelente')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    series = models.IntegerField(default=3)
    peso_agregado_KG = models.FloatField(default=0, null=True, blank=True)
    repeticiones_en_la_primera_serie = models.IntegerField(default=0)
    repeticiones_en_la_segunda_serie = models.IntegerField(default=0)
    repeticiones_en_la_tercera_serie = models.IntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)
    rendimiento_percibido = models.IntegerField(choices=RENDIMIENTO_CHOICES, default=3)

    def clean(self):
        """Validar que el ejercicio pertenezca a la rutina seleccionada"""
        if self.ejercicio and self.rutina and self.ejercicio.rutina != self.rutina:
            raise models.ValidationError('El ejercicio debe pertenecer a la rutina seleccionada.')

    def __str__(self):
        return f"{self.usuario.username} - {self.ejercicio.nombre} - {self.fecha_hora}"

    class Meta:
        ordering = ['-fecha_hora']
