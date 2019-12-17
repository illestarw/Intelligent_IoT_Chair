import boto3
import json
from datetime import datetime, timezone, timedelta

# res
# {
#    weight_r
#    weight_l
#    dis_l
#    dis_r
#}

def lambda_handler(event, context):
    # init
    isSitting = False
    now = datetime.now()
    notEnoughRestAlert = False
    sedentaryAlert = False
    
    # get param
    weight_r = float(event['weight_r'])
    weight_l = float(event['weight_l'])
    
    if event.get('init_sit_time') and event.get('init_sit_time') != "NA":
        init_sit_t = datetime.strptime(event['init_sit_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        duration_init = now - init_sit_t
        duration_init_s = duration_init.total_seconds()
    else:
        init_sit_t = "NA"
        duration_init_s = 0
    
    if event.get('leave_chair_time') and event.get('leave_chair_time') != "NA":
        leave_chair_t = datetime.strptime(event['leave_chair_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        duration_leave = now - init_sit_t
        duration_leave_s = duration_leave.total_seconds()
    else:
        leave_chair_t = "NA"
        duration_leave_s = 0
    
    if event.get('inalert'):
        inAlert = event['inalert']
    else:
        inAlert = False
        
    if event.get('lastsitstat'):
        wasSitting = event['lastsitstat']
    else:
        wasSitting = False
    
    
    # get total weight 
    weight = weight_r + weight_l
    
    if weight > 20:
        isSitting = True
    
    
    # when overtime alert is ON (user sit on chair over 1 hr)
    if inAlert:
        # stand up
        if wasSitting and not isSitting:
            # update time of user stand up
            leave_chair_t = now
        
        # sit down
        elif not wasSitting and isSitting:
            d = now - leave_chair_t
            if d.total_seconds() > 300: # 5 mins = 300 secs
                # reset timer and alert status
                init_sit_t = now
                leave_chair_t = "NA"
                inAlert = False
            else:
                # alert not enough rest
                notEnoughRestAlert = True
        
        # chair idle for enough rest time 
        elif not wasSitting and not isSitting:
            d = now - leave_chair_t
            if d.total_seconds() > 300: # 5 mins = 300 secs
                # reset timer and alert status
                init_sit_t = "NA"
                leave_chair_t = "NA"
                inAlert = False
    
    # when overtime alert is OFF
    else:
        # sit down
        if not wasSitting and isSitting:
            init_sit_t = now
        # stand up
        if wasSitting and not isSitting:
            # reset timer
            init_sit_t = "NA"
        # sit over 1 hr
        if wasSitting and isSitting and (duration_init_s > 3600): # 1 hr = 3600 secs
            inAlert = True
            sedentaryAlert = True
    
    if notEnoughRestAlert:
        message = "Sedentary Alert! It seems that you did not take enough rest. We suggest a least of 5 minutes for maintaining healthy conditions."
    elif sedentaryAlert:
		# timezone fix (UTC-8 Zone)
        init_sit_t_timezone = init_sit_t - timedelta(hours=8)
        message = "Sedentary Alert! You have been sitting on the chair since " + init_sit_t_timezone.strftime("%b %-d, %Y, %H:%M:%S") + ". We suggest you to leave your chair 5 minutes, do some stretchings, and maybe get yourself some coffee."
    else:
        message = "N/A"
    
    # serialize time
    if hasattr(init_sit_t, 'isoformat'):
        init_sit_format = init_sit_t.isoformat() + 'Z'
    else:
        init_sit_format = init_sit_t
    
    if hasattr(leave_chair_t, 'isoformat'):
        leave_chair_format = leave_chair_t.isoformat() + 'Z'
    else:
        leave_chair_format = leave_chair_t
    
    
    return {
        'lastsitstat': isSitting,
        'inalert': inAlert,
        'msg': message,
        'init_sit_time': init_sit_format,
        'leave_chair_time': leave_chair_format,
        'SNSAlert': sedentaryAlert or notEnoughRestAlert
    }