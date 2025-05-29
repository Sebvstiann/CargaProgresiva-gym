from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.registrar_entrenamiento, name='registrar_entrenamiento'),
    path('ver-registros/', views.ver_registros, name='ver_registros'),
    path('eliminar-registro/<int:registro_id>/', views.eliminar_registro, name='eliminar_registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('obtener-progreso/<int:ejercicio_id>/', views.obtener_progreso, name='obtener_progreso'),
]
