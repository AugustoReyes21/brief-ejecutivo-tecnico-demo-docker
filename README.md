# Brief Ejecutivo-Tecnico + Demo Docker

Caso aplicado: `e-commerce omnicanal`

Este repositorio contiene la documentacion principal y una demo practica event-driven con Docker Compose.

- `docs/brief.md`: brief ejecutivo-tecnico en Markdown
- `docker-compose.yml`: demo practica event-driven
- `docs/diagrams/`: diagramas Mermaid en archivos separados

## Estructura

```text
.
├── README.md
├── docker-compose.yml
├── docs
│   ├── brief.md
│   └── diagrams
│       ├── architecture.md
│       └── event-flow.md
└── services
    ├── erp-service
    │   ├── Dockerfile
    │   ├── app.py
    │   └── requirements.txt
    └── storefront-service
        ├── Dockerfile
        ├── app.py
        └── requirements.txt
```

## Como correr la demo

Requisito: Docker Desktop activo.

```bash
docker compose up --build
```

Cuando los contenedores esten arriba:

1. Crear una orden desde el front office:

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

2. Verificar que el ERP consumio el evento:

```bash
curl http://localhost:8001/orders
```

3. Evidencia esperada:

- Log en `storefront-service`: publicacion de `order_created`
- Log en `erp-service`: consumo del evento
- Respuesta HTTP en `http://localhost:8001/orders` con la orden registrada

Para detener la demo:

```bash
docker compose down
```

## Servicios de la demo

- `storefront-service`: front office que recibe la orden y publica el evento
- `redis`: broker simple para el flujo event-driven
- `erp-service`: sistema nucleo que consume el evento y registra la orden

## Checklist para el video

En el video deberias mostrar, en este orden:

1. La estructura del repositorio.
2. `docs/brief.md` y al menos un diagrama Mermaid renderizado.
3. `docker compose up --build` ejecutando sin errores.
4. El `curl` de creacion de orden.
5. Los logs de publicacion y consumo.
6. El `curl http://localhost:8001/orders`.
7. Un resumen de 30-60 segundos sobre gobierno, riesgo y metricas.

## Referencias oficiales usadas en la documentacion

- Mermaid: <https://mermaid.js.org/>
- GitHub Mermaid: <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams>
- COBIT: <https://www.isaca.org/resources/cobit>
- NIST CSF 2.0: <https://www.nist.gov/cyberframework>
- NIST SP 800-61 Rev. 3: <https://csrc.nist.gov/pubs/sp/800/61/r3/final>
- DORA metrics: <https://dora.dev/guides/dora-metrics-four-keys/>
- Google Cloud Four Keys: <https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance>
