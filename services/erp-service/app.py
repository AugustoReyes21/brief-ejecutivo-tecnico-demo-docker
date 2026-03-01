import json
import os
import threading
import time
import uuid

import redis
from flask import Flask, jsonify


app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
channel = os.getenv("REDIS_CHANNEL", "order-events")
port = int(os.getenv("PORT", "8001"))

consumed_orders = []


def get_redis_client():
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def subscriber_loop():
    while True:
        try:
            pubsub = get_redis_client().pubsub()
            pubsub.subscribe(channel)
            print(f"[erp-service] subscribed to channel={channel}", flush=True)

            for message in pubsub.listen():
                if message["type"] != "message":
                    continue

                event = json.loads(message["data"])
                record = {
                    "erp_receipt_id": str(uuid.uuid4()),
                    "received_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "event": event,
                }
                consumed_orders.append(record)
                print(
                    f"[erp-service] consumed {event['event_type']} "
                    f"event_id={event['event_id']} order_id={event['order']['order_id']}",
                    flush=True,
                )
        except redis.RedisError as exc:
            print(f"[erp-service] redis error: {exc}. retrying in 2s", flush=True)
            time.sleep(2)


@app.get("/health")
def health():
    return jsonify(
        {
            "service": "erp-service",
            "status": "ok",
            "consumed_orders": len(consumed_orders),
        }
    )


@app.get("/orders")
def orders():
    return jsonify({"count": len(consumed_orders), "orders": consumed_orders})


if __name__ == "__main__":
    subscriber = threading.Thread(target=subscriber_loop, daemon=True)
    subscriber.start()
    app.run(host="0.0.0.0", port=port, debug=False)
