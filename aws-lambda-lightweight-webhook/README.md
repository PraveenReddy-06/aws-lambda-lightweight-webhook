# AWS Lambda Function URLs — Lightweight Webhook

A lightweight serverless webhook receiver built with **AWS Lambda Function URLs**.

This project demonstrates how an HTTPS webhook endpoint can receive, validate, process, store, and observe events without running a dedicated backend server.

## Architecture

```text
Client / Postman / Browser
          |
          | HTTPS POST
          v
Lambda Function URL
          |
          v
      AWS Lambda
       /       \
      v         v
 DynamoDB   CloudWatch
```

## Implemented Features

- AWS Lambda with Python 3.14
- Lambda Function URL
- Webhook secret validation
- JSON validation
- Required-field validation
- DynamoDB event storage
- Atomic duplicate-event protection
- CloudWatch logging
- Postman test scenarios
- Minimal black-and-white browser frontend
- HTTP status handling

## HTTP Behavior

| Scenario | Status |
|---|---:|
| Valid webhook | 200 |
| Invalid secret | 401 |
| Missing body | 400 |
| Invalid JSON | 400 |
| Missing required fields | 400 |
| Duplicate eventId | 409 |

## Example Request

```json
{
  "eventId": "evt001",
  "eventType": "PROJECT_CREATED",
  "source": "KLInnovationHub",
  "data": {
    "projectName": "AI Attendance System"
  }
}
```

Header:

```text
X-Webhook-Secret: demo-secret
```

## AWS Configuration

### Lambda

- Function: `lightweight-webhook`
- Runtime: Python 3.14
- Handler: `lambda_function.lambda_handler`
- Region: `us-east-1`

### Environment Variables

```text
WEBHOOK_SECRET=<your-secret>
WEBHOOK_TABLE_NAME=webhook-events
```

Never commit a real secret to GitHub.

### DynamoDB

- Table: `webhook-events`
- Partition key: `eventId`
- Type: String

### IAM

The Lambda execution role requires `PutItem` permission for the `webhook-events` table. The implementation uses a conditional `PutItem` for atomic idempotency.

## Function URL

```text
https://6agmmwkz3qztsxp53276wwtcfy0qxkom.lambda-url.us-east-1.on.aws/
```

The endpoint is public. The webhook secret is the credential and must not be committed to the repository.

## Frontend

Open `frontend/index.html` in a browser or serve the frontend directory with a static web server.

For browser requests, configure CORS on the Lambda Function URL to allow the frontend origin.

## Testing

1. Valid webhook -> 200
2. Invalid secret -> 401
3. Missing body -> 400
4. Invalid JSON -> 400
5. Missing required fields -> 400
6. Repeat the same eventId -> 409
7. Send a new eventId -> 200

## Observability

CloudWatch log group:

```text
/aws/lambda/lightweight-webhook
```

## Production Security Extensions

- Store secrets in AWS Secrets Manager.
- Use provider-specific HMAC/signature verification.
- Restrict IAM permissions to required actions/resources.
- Restrict CORS to trusted frontend origins.
- Add request-size and schema validation.
- Add retention/TTL for stored events.

## Project Structure

```text
aws-lambda-lightweight-webhook/
├── lambda/
│   └── lambda_function.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── architecture/
│   └── architecture.md
├── README.md
└── .gitignore
```

## Demo

**HTTPS webhook -> Lambda -> validation -> DynamoDB idempotency -> CloudWatch logs**

No dedicated backend server is required.
