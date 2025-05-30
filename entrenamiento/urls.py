from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),
    path('perfil/', views.perfil, name='perfil'),
    path('actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('obtener-progreso/<int:ejercicio_id>/', views.obtener_progreso, name='obtener_progreso'),
    path('registrar-entrenamiento/', views.registrar_entrenamiento, name='registrar_entrenamiento'),
    path('ver-registros/', views.ver_registros, name='ver_registros'),
    path('exportar-registros/', views.exportar_registros_excel, name='exportar_registros_excel'),
    path('eliminar-registro/<int:registro_id>/', views.eliminar_registro, name='eliminar_registro'),
]
