# Architecture

```text
Postman / Browser / External Service
                |
                | HTTPS POST
                v
       AWS Lambda Function URL
                |
                v
           AWS Lambda
          /          \
         /            \
        v              v
   DynamoDB        CloudWatch
  event storage       logs
```

## Request flow

1. Function URL receives an HTTPS POST.
2. Lambda validates `X-Webhook-Secret`.
3. Lambda parses and validates the JSON payload.
4. DynamoDB atomically records `eventId`.
5. A repeated `eventId` returns HTTP 409.
6. CloudWatch receives Lambda execution logs.
