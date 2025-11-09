# DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)
## CARRERA DE INGENIERÍA EN SISTEMAS

---
### PROYECTO FINAL
### FRAMEWORK DE PRUEBAS AUTOMATIZADAS PARA SYLIUS
# Assurix  

---

## Tabla de Contenido

- [DIPLOMADO INGENIERÍA DE CALIDAD DE SOFTWARE COMERCIAL (3ra Edición)](#diplomado-ingeniería-de-calidad-de-software-comercial-3ra-edición)
  - [CARRERA DE INGENIERÍA EN SISTEMAS](#carrera-de-ingeniería-en-sistemas)
    - [PROYECTO FINAL](#proyecto-final)
    - [FRAMEWORK DE PRUEBAS AUTOMATIZADAS PARA SYLIUS](#framework-de-pruebas-automatizadas-para-sylius)
- [Assurix](#assurix)
  - [Tabla de Contenido](#tabla-de-contenido)
    - [1.Descripcion](#1descripcion)
    - [2.Estructura de Directorios del Proyecto](#2estructura-de-directorios-del-proyecto)
    - [3.Descripcion de Directorios Generales](#3descripcion-de-directorios-generales)
  - [4. Pruebas End-to-End (E2E)](#4-pruebas-end-to-end-e2e)
    - [Promociones](#promociones)
  - [5.Endpoints Evaluados por Sprint](#5endpoints-evaluados-por-sprint)
    - [Primer Sprint](#primer-sprint)
    - [Segundo Sprint](#segundo-sprint)
    - [6.Limites y Alcances](#6limites-y-alcances)
    - [7.Tipos de Mark Utilizados en el Proyecto](#7tipos-de-mark-utilizados-en-el-proyecto)
    - [Módulos / Dominios](#módulos--dominios)
    - [Prioridad](#prioridad)
    - [Tipo de Prueba](#tipo-de-prueba)
    - [8.Ejecucion de pruebas](#8ejecucion-de-pruebas)
    - [9.Autenticación y Obtención del Token](#9autenticación-y-obtención-del-token)
    - [10.Instalacion](#10instalacion)
  - [11.Buenas Practicas](#11buenas-practicas)
  - [12.Exploratoy Testing del API Spotify (Collection Postman)](#12exploratoy-testing-del-api-spotify-collection-postman)
  - [13.Autor](#13autor)
    

### 1.Descripcion
Este proyecto es un **framework de pruebas automatizadas para la REST API de Sylius**, construido con **Python** y `pytest`. Está diseñado para validar diferentes endpoints del panel administrativo de Sylius de forma estructurada, incorporando herramientas de generación de datos dinámicos, validación de respuestas y generación de reportes detallados mediante `Allure Reports`. Se basa en escenarios reales de uso de la API administrativa de Sylius, con el objetivo de garantizar la calidad, consistencia y confiabilidad de sus servicios REST.

### 2.Estructura de Directorios del Proyecto

```markdown
.
├── src/
│   ├── assertions/
│   │   ├── administrators/
│   │   │   ├── error_assertion.py
│   │   │   ├── schema_assertion.py
│   │   │   └── view_content_assertion.py
│   │   ├── product_reviews/
│   │   │   ├── error_assertion.py
│   │   │   ├── schema_assertion.py
│   │   │   └── view_content_assertion.py
│   │   ├── promotions/
│   │   │   ├── error_assertion.py
│   │   │   ├── schema_assertion.py
│   │   │   ├── view_content_assertion.py
│   │   │   ├── schemas_assertions.py
│   │   │   └── status_code_assertion.py
│   │   ├── schemas_assertions.py
│   │   └── status_code_assertion.py
│
│   ├── config/
│   │   ├── auth_token.py
│   │   └── config.py
│
│   ├── data/
│   │   ├── administrators.py
│   │   └── promotions.py
│
│   ├── resources/
│   │   ├── payloads/
│   │   │   ├── administrators_payload.py
│   │   │   ├── product_reviews_payload.py
│   │   │   └── promotions_payload.py
│   │   └── schemas/
│   │       ├── administrators/
│   │       ├── product_reviews/
│   │       └── promotions/
│
│   ├── routes/
│   │   ├── administrators_endpoint.py
│   │   ├── product_reviews_endpoint.py
│   │   ├── promotions_endpoint.py
│   │   └── endpoint.py
│
│   ├── services/
│   │   ├── call_request/
│   │   │   ├── administrators_call.py
│   │   │   ├── product_reviews_call.py
│   │   │   ├── promotions_call.py
│   │   │   └── __init__.py
│   │   └── request.py
│
│   └── utils/
│       ├── admin_helper.py
│       ├── load_resources.py
│       ├── logger_helpers.py
│       └── request_client.py
│
├── tests/
│   ├── administrators/
│   │   ├── avatar_images/
│   │   │   ├── test_HU07_NC_GET_Avatar_Images.py
│   │   │   ├── test_HU08_NC_POST_Avatar_Images.py
│   │   │   ├── test_HU09_NC_DELETE_Avatar_Images.py
│   │   │   ├── __init__.py
│   │   │   └── conftest.py
│   │   ├── test_HU02_NC_GET_Administrators.py
│   │   ├── test_HU03_NC_GET_Administrator.py
│   │   ├── test_HU04_NC_POST_Administrators.py
│   │   ├── test_HU05_NC_PUT_Administrators.py
│   │   ├── test_HU06_NC_DELETE_Administrators.py
│   │   ├── __init__.py
│   │   └── conftest.py
│
│   ├── marketing/
│   │   ├── product_reviews/
│   │   │   ├── test_HU17_NC_GET_ProductReviews.py
│   │   │   ├── test_HU18_NC_DELETE_ProductReviews.py
│   │   │   ├── __init__.py
│   │   │   └── conftest.py
│   │   └── promotions/
│   │       ├── test_HU10_NC_GET_Promotions.py
│   │       ├── test_HU11_NC_GET_Promotion.py
│   │       ├── test_HU12_NC_POST_Promotions.py
│   │       ├── test_HU13_NC_PUT_Promotions.py
│   │       ├── test_HU14_NC_PATCH_Promotions.py
│   │       ├── test_HU15_NC_DELETE_Promotions.py
│   │       ├── test_HU16_NC_DELETE_Promotions_Invalid.py
│   │       ├── __init__.py
│   │       └── conftest.py
│
│   ├── test_e2e/
│   │   ├── test_E2E_promocion_admin.py
│   │   ├── __init__.py
│   │   └── conftest.py
│
│   ├── conftest.py
│   └── __init__.py
│
├── reports/
├── venv/
├── .env
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

### 3.Descripcion de Directorios Generales
`src/:` Código fuente principal del framework<br>
`assertions/:` Validaciones y aserciones personalizadas<br>
`config/:` Configuración general y variables de entorno<br>
`data/:` Generación de datos dinámicos de prueba<br>
`resources/:` Payloads y esquemas JSON de validación<br>
`routes/:` Endpoints y rutas de la API<br>
`services/:` Peticiones HTTP hacia la API<br>
`utils/:` Funciones auxiliares y herramientas de soporte<br>
`tests/:` Casos de prueba automatizados por módulo<br>
`conftest.py:` Fixtures globales y autenticación de API<br>
`reports/:` Reportes generados por Allure o Pytest<br>
`pytest.ini:` Configuración y marcadores de Pytest<br>
`requirements.txt:` Dependencias del proyecto<br>
`.env:` Variables de entorno del framework<br>
`.gitignore:` Archivos ignorados por Git<br>
`README.md:` Documentación general del proyecto<br>

## 4. Pruebas End-to-End (E2E)

A continuación, se presenta el flujo evaluado dentro de las funcionalidades del módulo **Marketing – Promociones**.

### Promociones

- **POST** `/api/v2/admin/administrators/token`  
  Autentica al administrador y obtiene el token de acceso para las operaciones siguientes.

- **POST** `/api/v2/admin/promotions`  
  Crea una nueva promoción en el sistema administrativo de Sylius.

- **GET** `/api/v2/admin/promotions/{code}`  
  Consulta la información de la promoción recién creada.

- **PUT** `/api/v2/admin/promotions/{code}`  
  Actualiza los datos de la promoción (nombre, descripción, configuración, etc.).

- **PATCH** `/api/v2/admin/promotions/{code}/archive`  
  Archiva la promoción para desactivarla temporalmente.

- **PATCH** `/api/v2/admin/promotions/{code}/restore`  
  Restaura la promoción previamente archivada, reactivándola en el sistema.

- **DELETE** `/api/v2/admin/promotions/{code}`  
  Elimina definitivamente la promoción del catálogo administrativo.

- **GET** `/api/v2/admin/promotions/{code}`  
  Verifica que la promoción haya sido eliminada exitosamente (debe retornar un estado **404 Not Found**).

## 5.Endpoints Evaluados por Sprint

### Primer Sprint
| Autor     | Categoría         | Método | Endpoint                                         |
|------------|------------------|--------|--------------------------------------------------|
| Noelia Cantarran Villarroel     | ADMINISTRATORS   | GET    | /api/v2/admin/administrators                     |
| Noelia Cantarran Villarroel     | ADMINISTRATORS   | GET    | /api/v2/admin/administrators/{id}                |
| Noelia Cantarran Villarroel     | ADMINISTRATORS   | POST   | /api/v2/admin/administrators                     |
| Noelia Cantarran Villarroel    | ADMINISTRATORS   | PUT    | /api/v2/admin/administrators/{id}                |
| Noelia Cantarran Villarroel   | ADMINISTRATORS   | DELETE | /api/v2/admin/administrators/{id}                |
| Noelia Cantarran Villarroel   | AVATAR IMAGES    | GET    | /api/v2/admin/administrators/{id}/avatar-image  |
| Noelia Cantarran Villarroel     | AVATAR IMAGES    | POST   | /api/v2/admin/administrators/{id}/avatar-image  |
| Noelia Cantarran Villarroel   | AVATAR IMAGES    | DELETE | /api/v2/admin/administrators/{id}/avatar-image |

### Segundo Sprint
| Autor     | Categoría        | Método | Endpoint                                         |
|------------|-----------------|--------|--------------------------------------------------|
| Noelia Cantarran Villarroel    | PROMOTIONS      | GET    | /api/v2/admin/promotions                         |
| Noelia Cantarran Villarroel    | PROMOTIONS      | GET    | /api/v2/admin/promotions/{code}                  |
| Noelia Cantarran Villarroel    | PROMOTIONS      | POST   | /api/v2/admin/promotions                         |
| Noelia Cantarran Villarroel    | PROMOTIONS      | PUT    | /api/v2/admin/promotions/{code}                  |
| Noelia Cantarran Villarroel     | PROMOTIONS      | PATCH  | /api/v2/admin/promotions/{code}/archive          |
| Noelia Cantarran Villarroel    | PROMOTIONS      | PATCH  | /api/v2/admin/promotions/{code}/restore          |
|Noelia Cantarran Villarroel    | PROMOTIONS      | DELETE | /api/v2/admin/promotions/{code}                  |
| Noelia Cantarran Villarroel     | PRODUCT REVIEWS | GET    | /api/v2/admin/product-reviews                    |
| Noelia Cantarran Villarroel    | PRODUCT REVIEWS | DELETE | /api/v2/admin/product-reviews/{id}               |
| Noelia Cantarran Villarroel    | E2E MARKETING   | MIXTO  | Flujo completo: autenticación, creación, consulta, actualización, archivado, restauración y eliminación de promoción |

### 6.Limites y Alcances 
Las pruebas se enfocaron en:
- Validación de respuesta HTTP (códigos 200,201,204, 400,401,403,404, 405, 409, 415, 422, 500)
- Validacion de los endpoints **GET, POST, PUT, PATCH y DELETE** sobre los módulos **Administrators**, **Promotions** y **Product Reviews**.
- Validacion de Estructura del JSON de respuesta
- Casos de pruebas caso positivo , negativos y valor limite
- Validacion de tiempo de respuesta 
- Validacion de payload de entrada y del payload de salida
- Validacion de schemas JSON : estructura esperada , tipos de dato  y campos requeridos / no requeridos
- Comprobación de autorización mediante token
- Ejecución de pruebas End-to-End (E2E) para validar flujos
- Uso de yield de Pytest para combinar la fase de ejecución con la limpieza final (teardown) en los tests


### 7.Tipos de Mark Utilizados en el Proyecto
El framework utiliza distintas marcas (`@pytest.mark`) para clasificar, filtrar y ejecutar las pruebas de manera organizada según su módulo, prioridad o tipo de validación.

### Módulos / Dominios
`administrator:` Pruebas del módulo Administrador (Administrators)<br>
`marketing:` Pruebas del módulo Marketing (Promotions y Product Reviews)<br>
`avatar_images:` Pruebas del submódulo de imágenes o avatares asociados al administrador<br>
`product_reviews:` Pruebas del módulo de Reseñas de Productos<br>
`promotions:` Pruebas del módulo de Promociones<br>

### Prioridad
`high:` Prioridad alta → pruebas críticas; si fallan, bloquean la operación principal del sistema<br>
`medium:` Prioridad media → pruebas importantes; su falla afecta parcialmente las funcionalidades<br>
`low:` Prioridad baja → pruebas secundarias; su falla no impacta el negocio principal<br>

### Tipo de Prueba
`functional_positive:` Verifica el comportamiento correcto con entradas válidas<br>
`functional_negative:` Evalúa la respuesta ante entradas o condiciones no válidas<br>
`functional_validation:` Valida campos individuales y reglas de negocio<br>
`functional_edgecase:` Considera casos límite o valores extremos<br>
`security:` Evalúa autenticación, permisos y manejo de tokens<br>
`regression:` Reejecuta funcionalidades para asegurar que los cambios no introduzcan errores<br>
`e2e:` Pruebas End-to-End para validar flujos completos de negocio<br>
`concurrent:` Marca personalizada para pruebas concurrentes (por ejemplo, eliminaciones simultáneas)<br>

### 8.Ejecucion de pruebas

1. Ejecuta todos los archivos de prueba
```python

pytest -v

```
2.  Ejecuta el archivo reporte.html
```python

pytest --html=report.html

```

3. Ejecutar por archivo especifico
```python

pytest -s tests/administrators/test_HU02_NC_GET_Administrators.py

```

4. Ejecutar por el mark "administrator"
```python

pytest -m administrator --alluredir=reports/allure-results -v

```
5. Ejecutar por el mark "avatar_images"
```python

pytest -m avatar_images --alluredir=reports/allure-results -v

```

6. Ejecutar por el mark "promotions"
```python

pytest -m promotions --alluredir=reports/allure-results -v

```
7. Ejecutar por el mark "product_reviews"
```python

pytest -m product_reviews --alluredir=reports/allure-results -v

```
8. Ejecutar únicamente las pruebas End-to-End (E2E)
```python

pytest -m e2e --alluredir=reports/allure-results -v

```
9. Ejecutar todos los archivos de prueba y generar reportes allure y html
```python

pytest -v -s --alluredir=reports/allure-results --html=reports/resultados.html --self-contained-html

```
10. Ejecutar solo el módulo Marketing y generar reporte HTML
```python

pytest -v -s .\tests\marketing\ --html=reports/marketing_resultados.html --self-contained-html
```
11. Generar y visualizar reporte dinámico con Allure
```python

allure serve reports/allure-results

```
12. Abrir manualmente un reporte Allure previamente generado
```python

allure open reports/allure-report
```

### 9.Autenticación y Obtención del Token

Las pruebas requieren un **token JWT válido** obtenido mediante la autenticación del administrador del sistema.  
Este token se genera a través del endpoint de login y se utiliza en los encabezados de autorización (`Authorization: Bearer <token>`) para todas las peticiones de la API durante la ejecución de las pruebas automatizadas.

Para ejecutar las pruebas es necesario obtener un **token JWT válido** mediante la autenticación del administrador del sistema. Este token se utiliza en el encabezado de autorización (`Authorization: Bearer <token>`) en todas las peticiones posteriores a la API.

**Método:** POST  
**URL:** https://v2.demo.sylius.com/api/v2/admin/administrators/token   

**Encabezados:**
    Content-Type: application/json
    Accept: application/json

**Cuerpo de la solicitud:**
```json
{
  "email": "api@example.com",
  "password": "sylius-api"
}
```

Respuesta exitosa (200):
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
El token JWT obtenido debe incluirse en los encabezados de autenticación para todas las solicitudes que requieran autorización, de la siguiente manera:

Authorization: Bearer &lt;token&gt;

### 10.Instalacion

1.Clonar el repositorio CatSoft
```python

git https://github.com/Asuriyu/PROYECTO-FINAL.git

cd PROYECTO-FINAL

```

2.Crear un entorno virtual
```python

python -m venv env 

```

3.Activar el entorno virtual
```python

env\Scripts\Activate.ps1

```
4. Instalar Dependencias necesarias para ejecutar el proyecto
```python

pip install -r requirements.txt

```
5. Configurar variables de entorno
```python
# URL base del entorno de pruebas
BASE_URL=https://v2.demo.sylius.com

# Credenciales del administrador Sylius (para autenticación JWT)
ADMIN_EMAIL=api@example.com
ADMIN_PASSWORD=sylius-api

```

## 11.Buenas Practicas

`Archivo Schema :` Archivo de almacenamiento de schemas entrada/salida  usados <br>
`Assertions:` Archivo de almacenamiento de codigo reutilizable <br>
`Logger:` Archivo donde se almacenan los logger INFO , DEBUG para que nos permitira debugear el codigo <br>
`Teardown:` Garantiza la correcta preparación y limpieza del entorno de pruebas.
<br>
`Principio SOLID (S y O):` Cada clase sigue una responsabilidad y una facilidad de modificacion futura<br>

## 12.Exploratoy Testing del API Spotify (Collection Postman)

Se realizó la **prueba exploratoria del API de Sylius**, siguiendo la documentación oficial disponible en su entorno demo.  
Durante este proceso se ejecutaron solicitudes **HTTP mediante Postman**, lo que permitió comprender el comportamiento de los endpoints administrativos, identificar posibles respuestas inesperadas y registrar hallazgos relevantes.  

A continuación, se presenta el archivo JSON exportado con la colección de endpoints evaluados durante la exploración.

[📄Ver Collection JSON](https://drive.google.com/drive/u/1/folders/1MtJWbse82XjqnZRuoElpv5UNdUBib-eG)

## 13.Autor
- Cantarran Villarroel Noelia [![GitHub](https://img.shields.io/badge/GitHub-Asuriyu-blue?logo=github)](https://github.com/Asuriyu)