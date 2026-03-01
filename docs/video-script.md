# Guion de Video (3-5 min)

## 1. Apertura (20-30 s)

Hola, esta es mi entrega del `Brief Ejecutivo-Tecnico + Demo Docker`.
El caso aplicado es un `e-commerce omnicanal`.
Mi objetivo fue convertir el mapa de arquitectura del curso en una propuesta de decision TI y demostrar un flujo real de integracion `event-driven`.

## 2. Mostrar repositorio (30-40 s)

En pantalla muestro:

- `README.md`
- `docs/brief.md`
- `docs/diagrams/`
- `docker-compose.yml`
- `services/storefront-service`
- `services/erp-service`

Decir:

`Aqui esta la estructura pedida por la rubrica. La documentacion principal esta en Markdown y los diagramas estan en Mermaid.`

## 3. Mostrar Mermaid renderizado (20-30 s)

Abrir `docs/brief.md` en GitHub o en un editor con preview.

Decir:

`Este diagrama muestra el ERP como System of Record, los sistemas satelite de front office y back office, y el flujo hacia BI. En la demo implemento el flujo order_created entre el front office y el ERP usando eventos.`

## 4. Correr Docker Compose (30-40 s)

Ejecutar:

```bash
docker compose up --build
```

Decir:

`La demo tiene tres servicios: storefront-service, redis como broker simple y erp-service. La rubrica pide al menos dos sistemas y una integracion; aqui hay dos sistemas de negocio y un flujo event-driven demostrable.`

## 5. Probar el flujo (60-90 s)

Ejecutar:

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-100",
    "channel": "web",
    "items": [
      {"sku": "SKU-CHAIR-01", "qty": 2, "price": 49.90}
    ],
    "total": 99.80
  }'
```

Luego mostrar logs del `storefront-service` y del `erp-service`.

Despues ejecutar:

```bash
curl http://localhost:8001/orders
```

Decir:

`Aqui se ve que el front office publica el evento order_created y el ERP lo consume y lo registra. La ventaja es menor acoplamiento y posibilidad de agregar nuevos consumidores; la desventaja es que se necesita mejor observabilidad y manejo de consistencia eventual.`

## 6. Resumen de gobierno, riesgo y metricas (30-60 s)

Decir:

`En gobierno, defino roles claros, decisiones criticas y politicas minimas para accesos, cambios, backups, incidentes y proveedores.`

`En riesgo y seguridad, uso NIST CSF 2.0 con perfil actual versus objetivo y priorizo MFA, RBAC, secretos, logging y pruebas de restauracion.`

`En metricas, uso Deployment Frequency y Lead Time for Changes de DORA, mas MTTR y tasa de restauraciones exitosas para operacion y continuidad.`

## 7. Cierre (10-15 s)

Decir:

`Con esto cierro la demostracion de la arquitectura propuesta, su gobierno minimo viable y una prueba practica de integracion ejecutandose en Docker Compose.`
