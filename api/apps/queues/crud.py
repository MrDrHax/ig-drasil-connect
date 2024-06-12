from fastapi import HTTPException
import markdown
import requests
from sqlalchemy.orm import Session
from . import models
import boto3
from datetime import datetime, timedelta
import pytz
from cache.cache_object import cachedData
import json

from config import Config

import logging
logger = logging.getLogger(__name__)

tz = pytz.timezone('America/Mexico_City')

async def queues_answer_time():
    availableQueues = ["Tickets Management", "Customize Assistance", "Event News", "Default Queue","Supervisor", "Callback"]

    client = boto3.client('connect')
    queues = client.list_queues(
        InstanceId = Config.INSTANCE_ID,
    )

    myQueues = []
    myQueuesDic = {}
    for queue in queues['QueueSummaryList']:
        if queue['QueueType'] == "STANDARD":
            if queue['Name'] in availableQueues:
                myQueues.append(queue)
                myQueuesDic[queue['Id']] = queue['Name']

    queues_data = client.get_metric_data_v2(
        # InstanceId = Config.INSTANCE_ID,
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
        StartTime = datetime.now() - timedelta(days=34),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [{
            'FilterKey': 'QUEUE',
            'FilterValues': [queue['Id'] for queue in myQueues],
        }],
        Groupings = ['QUEUE'],
        Metrics = [
            {
                'Name': 'AVG_QUEUE_ANSWER_TIME'
            }
        ]
    )

    queue_series =[]
    categories = []
    for queue in queues_data['MetricResults']:
        # Try to get the value and if it doesn't exist, set it to 0
        try:
            queue['Collections'][0]['Value']
        except:
            queue['Collections'][0]['Value'] = 0
        
        queue_series.append(models.SeriesData(name = myQueuesDic[queue['Dimensions']['QUEUE']], 
                                              data=[queue['Collections'][0]['Value']]))
        categories.append(myQueuesDic[queue['Dimensions']['QUEUE']])


    queue_xaxis = models.XAxisData(
        categories = categories
    )

    queue_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = queue_xaxis
    )

    queue_chart = models.ChartData(
        type = "bar",
        series = queue_series,
        options = queue_options
    )

    queue_graph = models.GenericGraph(
        title = "Queue Answer Time",
        description = "The average time it takes for a call to be answered by queue.",
        footer = ("Updated at: " + datetime.now(tz).strftime("%H:%M")),
        chart = queue_chart
    )

    return queue_graph
cachedData.add("queues_answer_time", queues_answer_time, 30)

async def queues_contact_duration():
    availableQueues = ["Tickets Management", "Customize Assistance", "Event News", "Default Queue","Supervisor", "Callback"]

    client = boto3.client('connect')
    queues = client.list_queues(
        InstanceId = Config.INSTANCE_ID,
    )

    myQueues = []
    myQueuesDic = {}
    for queue in queues['QueueSummaryList']:
        if queue['QueueType'] == "STANDARD":
            if queue['Name'] in availableQueues:
                myQueues.append(queue)
                myQueuesDic[queue['Id']] = queue['Name']

    queues_data = client.get_metric_data_v2(
        # InstanceId = Config.INSTANCE_ID,
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
        StartTime = datetime.now() - timedelta(days=34),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [{
            'FilterKey': 'QUEUE',
            'FilterValues': [queue['Id'] for queue in myQueues],
        }],
        Groupings = ['QUEUE'],
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION'
            }
        ]
    )

    queue_series =[]
    categories = []
    for queue in queues_data['MetricResults']:
        queue_series.append(models.SeriesData(name = myQueuesDic[queue['Dimensions']['QUEUE']], 
                                              data=[queue['Collections'][0]['Value']]))
        categories.append(myQueuesDic[queue['Dimensions']['QUEUE']])


    queue_xaxis = models.XAxisData(
        categories = categories
    )

    queue_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = queue_xaxis
    )

    queue_chart = models.ChartData(
        type = "bar",
        series = queue_series,
        options = queue_options
    )

    queue_graph = models.GenericGraph(
        title = "Queue average contact duration",
        description = "The average time it takes for a call to be finished by queue.",
        footer = ("Updated at: " + datetime.now(tz).strftime("%H:%M")),
        chart = queue_chart
    )

    return queue_graph
cachedData.add("queues_contact_duration", queues_contact_duration, 30)
