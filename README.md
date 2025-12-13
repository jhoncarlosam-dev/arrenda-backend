# Arrendia Core – Backend MVP

Backend MVP para la **gestión de arriendos en Colombia y LATAM**, enfocado en pequeños y medianos propietarios que hoy operan con Excel, cuadernos y WhatsApp.

Este proyecto no depende de un framework específico. Está diseñado para ser **escalable, portable y defendible** a nivel técnico y de negocio.

---

## 🎯 Objetivo

Construir una **API backend sólida** que permita:

* Ordenar la gestión de arriendos
* Registrar pagos y comprobantes
* Mantener historial verificable
* Generar datos estructurados y valiosos

El foco inicial es **resolver un problema real**, no vender software.

---

## 🧩 Problema que resuelve

En Colombia y LATAM:

* La gestión de arriendos es mayormente informal
* No hay trazabilidad de pagos
* Existen conflictos frecuentes entre dueños e inquilinos
* No hay datos confiables para análisis financiero o de riesgo

Este backend convierte procesos manuales en información estructurada.

---

## 💡 Propuesta de Valor

* Uso gratuito para propietarios
* Registro claro de propiedades, contratos y pagos
* Comprobantes digitales de pago
* Historial accesible y verificable
* Base preparada para análisis de datos anonimizados

---

## 🧠 Principios del Proyecto

* API First (diseño antes del código)
* Dominio basado en casos reales
* Separación clara de responsabilidades
* Seguridad por defecto
* Escalabilidad consciente

---

## 🗂️ Dominio del Negocio

### Entidades principales

* Owner (Propietario)
* Property (Propiedad)
* Tenant (Inquilino)
* Contract (Contrato de arriendo)
* Payment (Pago)
* PaymentMethod (Método de pago)
* Receipt (Comprobante)

El diseño parte de situaciones reales: pagos en efectivo, Nequi, Bancolombia y comprobantes simples.

---

## 🔌 API Design

* Estilo REST
* Versionado (`/api/v1`)
* Contratos claros (request/response)
* Uso correcto de códigos HTTP

### Endpoints iniciales

* `/auth`
* `/owners`
* `/properties`
* `/tenants`
* `/contracts`
* `/payments`
* `/payments/{id}/receipt`

La API se documenta con **OpenAPI (Swagger)**.

---

## 🗄️ Base de Datos

* Enfoque relacional (PostgreSQL)
* Modelado normalizado
* Historial de pagos y contratos
* Preparado para escalar y auditar

Migraciones controladas mediante Flyway o Liquibase.

---

## 🔐 Seguridad

* Autenticación con JWT
* Autorización basada en roles
* Endpoints protegidos
* Configuración correcta de CORS

La seguridad no es un parche, es parte del diseño.

---

## ⚙️ Stack Técnico Inicial

* Java 17
* Spring Boot
* Spring Web
* Spring Security
* JPA / Hibernate
* PostgreSQL
* Docker

El stack puede cambiar sin romper el modelo mental del sistema.

---

## 📈 Escalabilidad

* API stateless
* Preparación para caching
* Diseño compatible con colas y procesos async
* Base lista para análisis de datos

No se optimiza prematuramente, pero se deja el camino abierto.

---

## 🧪 Testing

* Pruebas de API
* Validación de contratos
* Casos borde y errores controlados

Testing como parte del flujo, no al final.

---

## 🚀 Roadmap Inicial

1. Modelado del dominio
2. Diseño de la API
3. Persistencia y migraciones
4. CRUD base
5. Registro de pagos y comprobantes
6. Seguridad
7. Infraestructura y deploy

---

## 📌 Nota Final

Este proyecto nace de un caso real de arriendo.

No es un demo académico.
Es la base de una plataforma pensada para el mundo real en LATAM.
