import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

# res
# {
#    weight_r
#    weight_l
#    dis_l
#    dis_r
#}

def lambda_handler(event, context):
    # init
    message = "N/A"
    distanceAlert = False
    
    # get param
    dis_l = float(event['dis_l'])
    dis_r = float(event['dis_r'])
    
    # get distance 
    laptop_edge_dis = 30
    
	# trapezoid calculation
    distance = (dis_l + dis_r) / 2 + laptop_edge_dis
    
    if distance < 51:
        isTooClose = True
        distanceAlert = True
        message = "You may be staying too close to the monitor (approx. " + str(distance) + " cm detected). We suggest positioning your eyes at least 20 inches (51 cm) from the monitor."
    else:
        isTooClose = False
        
    # if already in tooClose state, suppress alert
    if isTooClose and event.get('lastdis'):
        distanceAlert = False
    
    return {
        'last': isTooClose,
        'SNSAlert': distanceAlert,
        'msg': message
    }