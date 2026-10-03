import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "demo-secret")
TABLE_NAME = os.environ.get("WEBHOOK_TABLE_NAME", "webhook-events")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    headers = event.get("headers") or {}
    normalized_headers = {str(k).lower(): v for k, v in headers.items()}

    if normalized_headers.get("x-webhook-secret") != WEBHOOK_SECRET:
        print("Unauthorized webhook request")
        return response(401, {
            "success": False,
            "message": "Invalid webhook secret"
        })

    body = event.get("body")
    if not body:
        return response(400, {
            "success": False,
            "message": "Request body is missing"
        })

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return response(400, {
            "success": False,
            "message": "Invalid JSON payload"
        })

    event_id = payload.get("eventId")
    event_type = payload.get("eventType")
    source = payload.get("source")
    data = payload.get("data")

    if not event_id or not event_type or not source:
        return response(400, {
            "success": False,
            "message": "eventId, eventType and source are required"
        })

    item = {
        "eventId": event_id,
        "eventType": event_type,
        "source": source,
        "data": data if data is not None else {},
        "processedAt": datetime.now(timezone.utc).isoformat()
    }

    try:
        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(eventId)"
        )
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code")

        if error_code == "ConditionalCheckFailedException":
            print(f"Duplicate event received: {event_id}")
            return response(409, {
                "success": False,
                "message": "Duplicate event",
                "eventId": event_id
            })

        print(f"DynamoDB error: {exc}")
        return response(500, {
            "success": False,
            "message": "Failed to store webhook event"
        })

    print("Webhook received")
    print(f"Event ID: {event_id}")
    print(f"Event Type: {event_type}")
    print(f"Source: {source}")
    print(f"Data: {data}")

    return response(200, {
        "success": True,
        "message": "Webhook processed successfully",
        "eventId": event_id
    })
