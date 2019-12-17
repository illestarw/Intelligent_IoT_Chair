import boto3
import json

def lambda_handler(event, context):
    
    client = boto3.client('iot-data', region_name='us-west-2')
    
    if event.get('lastdis') is False:
        lastdis = False
    else:
        lastdis = True
    
    
    response = client.publish(
        topic='status/distance',
        qos=0,
        payload=json.dumps({"lastdis" : lastdis})
    )
