# Proyecto Cotización Huellas

Este proyecto es una plataforma de cotización para **Huellas Litográficas** desarrollado con **Django**, **Next.js**, y **MySQL**. La plataforma permite la gestión de clientes, productos, materiales, máquinas de impresión y cotizaciones.

## Tecnologías Utilizadas
- **Backend**: Django con Django REST Framework
- **Frontend**: Next.js
- **Base de Datos**: MySQL
- **Estilos**: CSS (Tailwind o Sass opcional)

## Estructura de Carpetas
Consulta la estructura de carpetas en la documentación de [docs/README.md](docs/README.md).

## Instalación

### Backend (Django)
1. Crea un entorno virtual e instala las dependencias:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Configura las variables de entorno en un archivo `.env` basado en `.env.example`.

3. Ejecuta las migraciones e inicia el servidor de desarrollo:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

### Frontend (Next.js)
1. Instala las dependencias:
    ```bash
    cd frontend
    npm install
    ```

2. Inicia el servidor de desarrollo de Next.js:
    ```bash
    npm run dev
    ```

### Base de Datos (MySQL)
Ejecuta el script SQL en `database/init.sql` para inicializar las tablas necesarias (opcional).

## Documentación Adicional
- [Diagrama ER](docs/ERD.md)
- [Documentación de la API](docs/API.md)
