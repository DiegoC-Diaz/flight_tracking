# Pautas del Proyecto: Plane Tracker

Este documento proporciona una guía sobre las herramientas, estándares y flujos de trabajo utilizados en este proyecto. El objetivo es mantener una base de código consistente y facilitar la incorporación de nuevos desarrolladores.

## 1. Tecnologías Principales

El backend de este proyecto está construido con las siguientes tecnologías:

- **Python 3.10+**: Lenguaje de programación base.
- **FastAPI**: Framework web de alto rendimiento para construir APIs.
- **Poetry**: Herramienta para la gestión de dependencias y empaquetado.
- **Docker**: Plataforma para desarrollar, desplegar y ejecutar aplicaciones en contenedores.
- **Uvicorn**: Servidor ASGI (Asynchronous Server Gateway Interface) para ejecutar la aplicación FastAPI.

## 2. Calidad de Código

Para asegurar un código limpio, legible y libre de errores, utilizamos las siguientes herramientas. Es obligatorio ejecutar estas revisiones antes de integrar nuevo código.

- **Black**: Formateador de código automático. Asegura un estilo de código uniforme en todo el proyecto.
- **Ruff**: Linter de Python extremadamente rápido. Ayuda a detectar errores, bugs y problemas de estilo.
- **MyPy**: Comprobador de tipos estático. Ayuda a prevenir errores en tiempo de ejecución mediante el análisis de los tipos de variables y funciones.

## 3. Comandos y Flujo de Trabajo

Hemos definido una serie de comandos en el `Makefile` para simplificar las tareas comunes de desarrollo.

### Configuración Inicial

Para configurar el entorno de desarrollo local por primera vez, clona el repositorio e instala las dependencias usando Poetry:

```bash
# Instala todas las dependencias definidas en pyproject.toml
make install
```

### Ejecución de la Aplicación

Puedes ejecutar la aplicación de dos maneras:

1.  **Con Docker (Recomendado)**: Levanta todos los servicios (backend, base de datos, etc.) definidos en `docker-compose-dev.yml`.

    ```bash
    # Construye y levanta los contenedores en modo desarrollo
    make run-dev-build

    # O si los contenedores ya están construidos
    make run-dev
    ```

2.  **Localmente (Sin Docker)**: Ejecuta la aplicación FastAPI directamente en tu máquina.

    ```bash
    # Inicia el servidor Uvicorn en http://localhost:8000
    make run-app
    ```

### Comandos de Calidad de Código

Utiliza estos comandos para formatear y analizar tu código antes de hacer commit.

```bash
# Aplica el formato de Black al código
make formatter

# Ejecuta el linter Ruff para detectar problemas
make lint

# Ejecuta el comprobador de tipos MyPy
make mypy
```

### Resumen de Comandos del Makefile

| Comando         | Descripción                                                                 |
| --------------- | --------------------------------------------------------------------------- |
| `install`       | Instala las dependencias del proyecto con Poetry.                           |
| `run-app`       | Ejecuta la aplicación localmente sin Docker.                                |
| `run-dev`       | Levanta los servicios de desarrollo con Docker Compose.                     |
| `run-dev-build` | Reconstruye y levanta los servicios de desarrollo.                          |
| `stop-dev`      | Detiene los servicios de desarrollo de Docker.                              |
| `formatter`     | Aplica el formateo de código con Black.                                     |
| `lint`          | Ejecuta el linter (Ruff) y verifica el formato (Black).                     |
| `lint-fix`      | Intenta arreglar automáticamente los problemas detectados por Ruff.         |
| `mypy`          | Ejecuta la comprobación de tipos estáticos con MyPy.                        |

