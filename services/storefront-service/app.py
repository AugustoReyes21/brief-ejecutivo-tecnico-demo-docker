import json
import os
import time
import uuid

import redis
from flask import Flask, jsonify, request


app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)
channel = os.getenv("REDIS_CHANNEL", "order-events")
port = int(os.getenv("PORT", "8000"))


@app.get("/health")
def health():
    return jsonify({"service": "storefront-service", "status": "ok"})


@app.post("/orders")
def create_order():
    payload = request.get_json(silent=True) or {}
    required_fields = ["customer_id", "channel", "items", "total"]
    missing_fields = [field for field in required_fields if field not in payload]

    if missing_fields:
        return (
            jsonify(
                {
                    "error": "missing required fields",
                    "missing_fields": missing_fields,
                }
            ),
            400,
        )

    event = {
        "event_type": "order_created",
        "event_id": str(uuid.uuid4()),
        "occurred_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "order": {
            "order_id": f"ORD-{int(time.time())}",
            "customer_id": payload["customer_id"],
            "channel": payload["channel"],
            "items": payload["items"],
            "total": payload["total"],
        },
    }

    redis_client.publish(channel, json.dumps(event))
    print(
        f"[storefront-service] published {event['event_type']} "
        f"event_id={event['event_id']} order_id={event['order']['order_id']}",
        flush=True,
    )

    return (
        jsonify(
            {
                "message": "order received and event published",
                "channel": channel,
                "event": event,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)
