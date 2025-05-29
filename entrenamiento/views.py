# entrenamiento/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistroEntrenamientoForm
from .models import RegistroEntrenamiento, Rutina, Ejercicio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UsuarioRegistroForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = UsuarioRegistroForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
            register_form = UsuarioRegistroForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "¡Te has registrado correctamente! Ahora puedes iniciar sesión.")
                return redirect('login')
            else:
                # Si hay errores en el registro, mostrar el formulario con errores
                context = self.get_context_data()
                context['register_form'] = register_form
                return render(request, self.template_name, context)
        return super().post(request, *args, **kwargs)

@login_required
def registrar_entrenamiento(request):
    if request.method == 'POST':
        form = RegistroEntrenamientoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            messages.success(request, '✅ Entrenamiento guardado correctamente.')
            return redirect('registrar_entrenamiento')
        messages.error(request, '❌ Hubo un error al guardar el entrenamiento.')
    else:
        form = RegistroEntrenamientoForm()
    return render(request, 'entrenamiento/registrar_entrenamiento.html', {'form': form})

@login_required
def ver_registros(request):
    rutina_id = request.GET.get('rutina')
    ejercicio_id = request.GET.get('ejercicio')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    rutinas = Rutina.objects.all()
    ejercicios = Ejercicio.objects.all()

    # filtrar SOLO los registros de este usuario:
    registros = RegistroEntrenamiento.objects.filter(usuario=request.user)

    if rutina_id:
        registros = registros.filter(rutina_id=rutina_id)
    if ejercicio_id:
        registros = registros.filter(ejercicio_id=ejercicio_id)
    if fecha_inicio:
        registros = registros.filter(fecha_hora__date__gte=fecha_inicio)
    if fecha_fin:
        registros = registros.filter(fecha_hora__date__lte=fecha_fin)

    return render(request, 'entrenamiento/ver_registros.html', {
        'registros': registros,
        'rutinas': rutinas,
        'ejercicios': ejercicios,
        'rutina_seleccionada': int(rutina_id) if rutina_id else None,
        'ejercicio_seleccionado': int(ejercicio_id) if ejercicio_id else None,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

@login_required
def eliminar_registro(request, registro_id):
    registro = get_object_or_404(RegistroEntrenamiento, id=registro_id, usuario=request.user)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro eliminado correctamente.')
    return redirect('ver_registros')

@login_required
def perfil(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'entrenamiento/perfil.html', {
        'ejercicios': ejercicios
    })

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        if 'imagen' in request.FILES:
            request.user.imagen = request.FILES['imagen']
        if request.POST.get('email'):
            request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
    return redirect('perfil')

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
        elif new_password1 != new_password2:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login')
    return redirect('perfil')

@login_required
def obtener_progreso(request, ejercicio_id):
    registros = RegistroEntrenamiento.objects.filter(
        usuario=request.user,
        ejercicio_id=ejercicio_id
    ).order_by('fecha_hora')

    data = {
        'fechas': [r.fecha_hora.strftime('%d/%m/%Y') for r in registros],
        'pesos': [r.peso_agregado_KG for r in registros],
        'reps1': [r.repeticiones_en_la_primera_serie for r in registros],
        'reps2': [r.repeticiones_en_la_segunda_serie for r in registros],
        'reps3': [r.repeticiones_en_la_tercera_serie for r in registros],
    }
    
    return JsonResponse(data)
