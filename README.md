# Carga Progresiva - Aplicación de Seguimiento de Entrenamiento

Esta es una aplicación web desarrollada con Django para el seguimiento de entrenamientos y progreso en el gimnasio.

## Características

- Registro y autenticación de usuarios
- Seguimiento de entrenamientos
- Registro de ejercicios y series
- Visualización de progreso con gráficos
- Perfil de usuario personalizable
- Filtros para ver registros históricos

## Requisitos

- Python 3.8 o superior
- PostgreSQL
- Otras dependencias en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear y activar entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Linux/Mac
.\env\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos en settings.py

5. Realizar las migraciones:
```bash
python manage.py migrate
```

6. Crear un superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:
```bash
python manage.py runserver
```

## Uso

1. Acceder a http://localhost:8000
2. Registrarse o iniciar sesión
3. Comenzar a registrar entrenamientos

## Tecnologías Utilizadas

- Django
- PostgreSQL
- Bootstrap
- Chart.js
- Crispy Forms 