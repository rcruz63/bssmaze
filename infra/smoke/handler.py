"""Lambda de humo: comprueba permisos, DynamoDB y arranque en frío."""

import json
import os
import time
from typing import Any

import boto3

# Se mide en la importación: así se distingue la primera invocación (arranque en frío).
_INIT_AT = time.time()
_STATE = {"warm": False}
_TABLE = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    cold_start = not _STATE["warm"]
    _STATE["warm"] = True
    now = int(time.time())
    key = {"PK": f"SMOKE#{now}", "SK": "hello"}
    # El ttl de 1 hora evita que la prueba deje basura en la tabla.
    _TABLE.put_item(Item={**key, "ttl": now + 3600, "msg": "written by smoke lambda"})
    item = _TABLE.get_item(Key=key)["Item"]
    body = {
        "ok": True,
        "msg": "hello from telnet tales",
        "cold_start": cold_start,
        "ms_since_init": int((time.time() - _INIT_AT) * 1000),
        "item": {k: (int(v) if k == "ttl" else v) for k, v in item.items()},
    }
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }
