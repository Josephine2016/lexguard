"""AWS service layer with graceful local fallback.

- CaseStore: DynamoDB table `lexguard-cases` in prod, JSONL on disk in dev/demo.
- Notifier:     SNS topic + WhatsApp (End User Messaging / Twilio) in prod, print in dev.
- DocStore:     S3 bucket for generated complaint PDFs in prod, local folder in dev.
Set LEXGUARD_ENV=aws to enable real AWS calls (credentials via IAM role/keys).
"""
import json, os

ENV = os.environ.get("LEXGUARD_ENV", "local")

def _table():
    import boto3
    from ..config import TABLE
    return boto3.resource("dynamodb").Table(TABLE)

def put_case(case):
    if ENV == "aws":
        _table().put_item(Item=case)
    else:
        from ..actions import save_case
        from ..config import CASES_PATH
        save_case(case, CASES_PATH)

def notify(phone, text):
    if ENV == "aws":
        import boto3
        sns = boto3.client("sns")
        # In prod: publish to SNS -> Lambda -> WhatsApp Business API (End User Messaging)
        sns.publish(TopicArn=os.environ["LEXGUARD_SNS_TOPIC"], Message=text)
    else:
        print(f"[notify:{phone}] {text}")

def store_document(case_id, filename, body):
    if ENV == "aws":
        import boto3
        bucket = os.environ["LEXGUARD_S3_BUCKET"]
        boto3.client("s3").put_object(Bucket=bucket, Key=f"cases/{case_id}/{filename}", Body=body)
        return f"s3://{bucket}/cases/{case_id}/{filename}"
    os.makedirs("outbox", exist_ok=True)
    path = os.path.join("outbox", f"{case_id}_{filename}")
    with open(path, "w") as f:
        f.write(body)
    return path
