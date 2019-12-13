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
    imbalance = False
    message = "N/A"
    weightDiffAlert = False
    
    # get param
    weight_r = float(event['weight_r'])
    weight_l = float(event['weight_l'])
    
    # get weight load on the heavier side
    if weight_l > weight_r:
        weight_hside = weight_l
        hside = 'left'
    elif weight_l < weight_r:
        weight_hside = weight_r
        hside = 'right'
    else:
        weight_hside = weight_l
        hside = 'none'
    
    if abs(weight_r - weight_l) > weight_hside * 0.2:
        imbalance = True
        weightDiffAlert = True
        message = "Imperfect posture detected! You have been laying yourself on the " + hside + " side too much. We suggest rearranging yourself to sit in the middle and keep your back straight."
    
    # if already in imbalance state, suppress alert
    if imbalance and event.get('lastpos'):
        weightDiffAlert = False
    
    
    return {
        'lastpos': imbalance,
        'SNSAlert': weightDiffAlert,
        'msg': message
    }