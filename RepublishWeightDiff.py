import boto3
import json

def lambda_handler(event, context):
    
    client = boto3.client('iot-data', region_name='us-west-2')
    
    if event.get('lastpos') is False:
        lastpos = False
    else:
        lastpos = True
    
    
    response = client.publish(
        topic='status/posture',
        qos=0,
        payload=json.dumps({"lastpos" : lastpos})
    )
