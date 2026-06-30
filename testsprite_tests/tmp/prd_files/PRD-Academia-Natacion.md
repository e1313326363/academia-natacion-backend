# PRD — Sistema de Gestión Academia de Natación

## 1. Resumen del Producto

Sistema web full-stack para la gestión interna de una academia de natación. Permite administrar estudiantes, instructores, clases, inscripciones, pagos y asistencias desde un panel centralizado con autenticación local.

- **Frontend:** Angular 20 · Bootstrap 5 · `http://localhost:4200`
- **Backend:** Laravel 13 · REST API · `http://localhost:8000/api`
- **Base de datos:** MySQL · `academia_natacion`
- **Autenticación:** Laravel Sanctum (token Bearer, 100% local)

---

## 2. Usuarios y Roles

| Rol   | Descripción                                          |
|-------|------------------------------------------------------|
| Admin | Único rol. Acceso completo a todas las funcionalidades |

**Credenciales por defecto:** `admin@academia.com` / `admin123`

---

## 3. Arquitectura

```
┌─────────────────────┐        REST API        ┌──────────────────────┐
│   Angular 20 SPA    │ ◄────────────────────► │   Laravel 13 API     │
│   (puerto 4200)     │   Bearer Token (Sanctum)│   (puerto 8000)      │
└─────────────────────┘                         └──────────┬───────────┘
                                                           │
                                                 ┌─────────▼──────────┐
                                                 │  MySQL             │
                                                 │  academia_natacion  │
                                                 └────────────────────┘
```

---

## 4. Módulos y Funcionalidades

### 4.1 Autenticación

| Item | Detalle |
|------|---------|
| Ruta | `/login` |
| Campos | Email, Contraseña |
| Éxito | Token guardado en localStorage → redirige a `/dashboard` |
| Fallo | Muestra mensaje de error en pantalla |
| Logout | Botón en topbar → limpia token → redirige a `/login` |
| Protección | `AuthGuard` bloquea todas las rutas excepto `/login` |

---

### 4.2 Dashboard

| Item | Detalle |
|------|---------|
| Ruta | `/dashboard` |
| Tarjetas | Total estudiantes · Total instructores · Total clases · Inscripciones activas |
| Acceso rápido | Links directos a cada sección desde el sidebar y el dashboard |

---

### 4.3 Estudiantes

| Item | Detalle |
|------|---------|
| Ruta lista | `/estudiantes` |
| Ruta crear | `/estudiantes/nuevo` |
| Ruta editar | `/estudiantes/editar/:id` |
| Búsqueda | Por nombre o email |
| Paginación | Sí |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| nombre | Texto (máx. 80 car.) | ✅ |
| fecha_nacimiento | Fecha | ✅ |
| telefono | Texto | ❌ |
| email | Email | ❌ |

**Acciones:** Crear · Editar · Eliminar (con diálogo de confirmación)

**API endpoints:**
- `GET /api/estudiantes?search=&page=`
- `GET /api/estudiantes/{id}`
- `POST /api/estudiantes`
- `PUT /api/estudiantes/{id}`
- `DELETE /api/estudiantes/{id}`

---

### 4.4 Instructores

| Item | Detalle |
|------|---------|
| Ruta lista | `/instructores` |
| Ruta crear | `/instructores/nuevo` |
| Ruta editar | `/instructores/editar/:id` |
| Búsqueda | Por nombre |
| Paginación | Sí |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| nombre | Texto (máx. 80 car.) | ✅ |
| especialidad | Texto | ❌ |
| email | Email | ❌ |

**API endpoints:**
- `GET /api/instructores?search=&page=`
- `GET /api/instructores/{id}`
- `POST /api/instructores`
- `PUT /api/instructores/{id}`
- `DELETE /api/instructores/{id}`

---

### 4.5 Clases

| Item | Detalle |
|------|---------|
| Ruta lista | `/clases` |
| Ruta crear | `/clases/nuevo` |
| Ruta editar | `/clases/editar/:id` |
| Paginación | Sí |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| nombre_clase | Texto (máx. 100 car.) | ✅ |
| id_nivel | Select (Principiante / Intermedio / Avanzado / Competencia) | ✅ |
| id_instructor | Select (lista de instructores) | ✅ |
| cupo | Número (1–50) | ✅ |

**API endpoints:**
- `GET /api/clases?page=`
- `GET /api/niveles` (para poblar dropdown)
- `GET /api/instructores` (para poblar dropdown)
- `POST /api/clases`
- `PUT /api/clases/{id}`
- `DELETE /api/clases/{id}`

---

### 4.6 Inscripciones

| Item | Detalle |
|------|---------|
| Ruta lista | `/inscripciones` |
| Ruta crear | `/inscripciones/nueva` |
| Filtro | Por estado: Activo · Suspendido · Baja |
| Paginación | Sí |
| Acción inline | Cambiar estado directamente desde la tabla |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| id_estudiante | Select (lista de estudiantes) | ✅ |
| id_clase | Select (lista de clases) | ✅ |
| fecha_inscripcion | Fecha | ❌ |
| estado | Select (Activo / Suspendido / Baja) | ❌ |

**API endpoints:**
- `GET /api/inscripciones?estado=&page=`
- `POST /api/inscripciones`
- `PUT /api/inscripciones/{id}`
- `DELETE /api/inscripciones/{id}`

---

### 4.7 Pagos

| Item | Detalle |
|------|---------|
| Ruta lista | `/pagos` |
| Ruta crear | `/pagos/nuevo` |
| Filtro | Por estado: Pagado · Pendiente · Vencido |
| Paginación | Sí |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| id_inscripcion | Select (inscripciones activas) | ✅ |
| monto | Número decimal | ✅ |
| fecha_pago | Fecha | ❌ |
| metodo_pago | Select (Efectivo / Tarjeta / Transferencia) | ✅ |
| estado | Select (Pagado / Pendiente / Vencido) | ❌ |

**API endpoints:**
- `GET /api/pagos?estado=&page=`
- `POST /api/pagos`
- `DELETE /api/pagos/{id}`

---

### 4.8 Asistencias

| Item | Detalle |
|------|---------|
| Ruta lista | `/asistencias` |
| Ruta crear | `/asistencias/nueva` |
| Filtro | Por fecha de clase |
| Paginación | Sí |

**Campos del formulario:**

| Campo | Tipo | Requerido |
|-------|------|-----------|
| id_inscripcion | Select (inscripciones activas) | ✅ |
| fecha_clase | Fecha | ✅ |
| asistio | Radio (Sí / No) | ✅ |

**API endpoints:**
- `GET /api/asistencias?fecha_clase=&page=`
- `POST /api/asistencias`
- `DELETE /api/asistencias/{id}`

---

## 5. Base de Datos

| Tabla | PK | Relaciones |
|-------|----|------------|
| `Niveles` | id_nivel | hasMany Clases |
| `Instructores` | id_instructor | hasMany Clases |
| `Estudiantes` | id_estudiante | hasMany Inscripciones |
| `Clases` | id_clase | belongsTo Nivel, Instructor · hasMany Inscripciones |
| `Inscripciones` | id_inscripcion | belongsTo Estudiante, Clase · hasMany Pagos, Asistencias |
| `Pagos` | id_pago | belongsTo Inscripcion |
| `Asistencia` | id_asistencia | belongsTo Inscripcion |

---

## 6. Seguridad

- Toda la autenticación es **100% local** mediante Laravel Sanctum.
- No se usa ningún proveedor externo (Auth0, Firebase, OAuth, AWS Cognito, etc.).
- El token Bearer se almacena en `localStorage` y se inyecta en cada request via `AuthInterceptor`.
- Las rutas protegidas usan `AuthGuard`; un 401 del API dispara logout automático.
- CORS configurado solo para `http://localhost:4200`.

---

## 7. Flujo Principal de Usuario

```
/login
  └─► autenticación exitosa
        └─► /dashboard  (stats + navegación)
              ├─► /estudiantes  ──► /estudiantes/nuevo | /estudiantes/editar/:id
              ├─► /instructores ──► /instructores/nuevo | /instructores/editar/:id
              ├─► /clases       ──► /clases/nuevo       | /clases/editar/:id
              ├─► /inscripciones──► /inscripciones/nueva
              ├─► /pagos        ──► /pagos/nuevo
              └─► /asistencias  ──► /asistencias/nueva
```

---

## 8. Restricciones y Limitaciones

- Base de datos pre-existente: no se modifican nombres de tablas ni columnas.
- Solo existe el rol `admin`; no hay sistema de roles múltiples.
- Los pagos y asistencias no tienen pantalla de edición (solo crear y eliminar).
- Los dropdowns de inscripciones en Pagos y Asistencias muestran únicamente las de estado `Activo`.
