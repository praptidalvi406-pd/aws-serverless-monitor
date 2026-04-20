import urllib.request
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    SITE_URL = "https://www.google.com"
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

    sns = boto3.client('sns')
    cw = boto3.client('cloudwatch')

    try:
        response = urllib.request.urlopen(SITE_URL, timeout=5)
        status = 1 # UP [cite: 22]
    except Exception as e:
        status = 0 # DOWN [cite: 24]
        
        if SNS_TOPIC_ARN:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Alert: Site Down!",
                Message=f"Site {SITE_URL} failed at {datetime.now()}."
            ) [cite: 26-31]

    cw.put_metric_data(
        Namespace='HealthCheckApp',
        MetricData=[{
            'MetricName': 'SiteAvailability',
            'Value': status,
            'Unit': 'Count'
        }]
    ) [cite: 32-36]

    return {"status": status} [cite: 37]
