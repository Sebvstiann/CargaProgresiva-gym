from django import forms
from .models import RegistroEntrenamiento
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Ejercicio

class UsuarioRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Usuario
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar los mensajes de ayuda
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
        
        self.fields['email'].label = 'Correo electrónico'
        self.fields['email'].help_text = 'Por favor, ingresa un correo electrónico válido.'
        
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].help_text = '''
            <ul>
                <li>Tu contraseña no puede ser muy similar a tu información personal.</li>
                <li>Tu contraseña debe contener al menos 8 caracteres.</li>
                <li>Tu contraseña no puede ser una contraseña comúnmente utilizada.</li>
                <li>Tu contraseña no puede ser completamente numérica.</li>
            </ul>
        '''
        
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña que antes, para verificación.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class RegistroEntrenamientoForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrenamiento
        fields = [
            'rutina', 'ejercicio',
            'peso_agregado_KG',
            'repeticiones_en_la_primera_serie', 
            'repeticiones_en_la_segunda_serie', 
            'repeticiones_en_la_tercera_serie',
            'observaciones', 
            'rendimiento_percibido'
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'style': 'resize: none;',
                'placeholder': 'Notas adicionales sobre el entrenamiento...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegistroEntrenamientoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'

        # Inicialmente, deshabilitamos el campo de ejercicio hasta que se seleccione una rutina
        self.fields['ejercicio'].queryset = Ejercicio.objects.none()
        self.fields['ejercicio'].widget.attrs['disabled'] = 'disabled'

        # Si hay una rutina seleccionada (en caso de edición o POST)
        if 'rutina' in self.data:
            try:
                rutina_id = int(self.data.get('rutina'))
                self.fields['ejercicio'].queryset = Ejercicio.objects.filter(rutina_id=rutina_id)
                self.fields['ejercicio'].widget.attrs.pop('disabled', None)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.rutina:
            self.fields['ejercicio'].queryset = Ejercicio.objects.filter(rutina=self.instance.rutina)
            self.fields['ejercicio'].widget.attrs.pop('disabled', None)


class CompletarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['peso', 'altura', 'edad', 'imagen']
        labels = {
            'peso': 'Peso (kg)',
            'altura': 'Altura (cm)',
            'edad': 'Edad',
            'imagen': 'Foto de Perfil'
        }
        widgets = {
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'onchange': 'previewImage(this)'
            })
        }
