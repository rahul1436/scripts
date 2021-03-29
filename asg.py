import boto3
import sys
from datetime import datetime, timedelta
from dateutil import tz

def get_cpu_util(instanceID,startTime,endTime):
    client = boto3.client('cloudwatch')
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
            'Name': 'InstanceId',
            'Value': instanceID
            },
        ],

        StartTime=startTime,
        EndTime=endTime,
        Period=86400,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )

    for k, v in response.items():
        if k == 'Datapoints':
            for y in v:
                return "{0:.2f}".format(y['Average'])


instanceIDs=[]

now = datetime.utcnow().date()
endTime = datetime(now.year, now.month, now.day, tzinfo=tz.tzutc())
startTime = endTime - timedelta(minutes=5)
avgs = list()

for instance in instanceIDs:
    avgs.append(get_cpu_util(instance,startTime,endTime))

per = (sum([float(a) for a in avgs]) / len(avgs))
print (per)
if per >= 80:
    print ("no need to modify aws asg")
else:
    client = boto3.client('autoscaling')
    response = client.set_desired_capacity(
        AutoScalingGroupName='test-base-on-cpu',
        DesiredCapacity=1,

    )
