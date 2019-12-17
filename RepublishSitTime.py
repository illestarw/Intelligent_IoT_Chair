import boto3
import json

  
def lambda_handler(event, context):
    
    client = boto3.client('iot-data', region_name='us-west-2')
    
    # init
    lastsitstat = inalert = False
    init_sit_time = leave_chair_time = "NA"
    
    if event.get('lastsitstat'):
        lastsitstat = event['lastsitstat']
    
    if event.get('inalert'):
        inalert = event['inalert']
        
    if event.get('init_sit_time'):
        init_sit_time = event['init_sit_time']
    
    if event.get('leave_chair_time'):
        leave_chair_time = event['leave_chair_time']
    
    res = {
        "lastsitstat": lastsitstat,
        "inalert": inalert,
        "init_sit_time": init_sit_time,
        "leave_chair_time": leave_chair_time
    }
    
    # Change topic, qos and payload
    response = client.publish(
        topic='status/sittime',
        qos=0,
        payload=json.dumps(res)
    )