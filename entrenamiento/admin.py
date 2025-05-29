from django.contrib import admin
from .models import Usuario, Rutina, Ejercicio, RegistroEntrenamiento

admin.site.register(Usuario)
admin.site.register(Rutina)
admin.site.register(Ejercicio)
admin.site.register(RegistroEntrenamiento)
