from sqlalchemy.orm import Session
from . import models
import boto3
from config import Config
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date
from tools.lazySquirrel import LazySquirrel

import logging
logger = logging.getLogger(__name__)


async def online_agents():
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Agents': userList
        }
    )

    count = 0
    for user in users_data['UserDataList']:
        if user['Status']['StatusName'] == "Available":
            count += 1

    if count <= 5:
        color = "text-red-500"
    else:
        color = "text-green-500"

    cardFooter = models.CardFooter(
        color = color,
        value= str(count),
        label="Available agents",
    )

    card = models.GenericCard(
        id=1,
        title="online agents",
        value= str(users_data['ApproximateTotalCount']),
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card
cachedData.add("online_agents", online_agents, 15)


async def need_assistance_agents():
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    count = 0
    assistanceCount = 0
    for user in users_data['UserDataList']:
        if user['Status']['StatusName'] == "Needs Assistance":
            count += 1
            if datetime.now(user['Status']['StatusStartTimestamp'].tzinfo) - user['Status']['StatusStartTimestamp'] >= timedelta(minutes=5):
                assistanceCount += 1
                


    if count >= 3:
        color = "text-red-500"
    else:
        color = "text-green-500"

    cardFooter = models.CardFooter(
        color = color,
        value= str(assistanceCount),
        label="have passed over 5 minutes wating for assistance",
    )

    card = models.GenericCard(
        id=1,
        title="Agents that need assistance",
        value= str(count),
        icon="HandRaisedIcon",
        footer=cardFooter,
    )

    return card
cachedData.add("need_assistance_agents", need_assistance_agents, 5)


async def queues_agent_answer_rate():
    userNT = ["94c89e21-3aac-44b5-8ffa-c898061fddfd"]

    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    userDic = {}
    for user in users['UserSummaryList']:
        if user['Id'] not in userNT:
            userList.append(user['Id'])
            userDic[user['Id']] = user['Username']


    user_data = client.get_metric_data_v2(
        # InstanceId = Config.INSTANCE_ID,
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
        StartTime = datetime.now() - timedelta(days=34),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [{
            'FilterKey': 'AGENT',
            'FilterValues': userList,
        }],
        Groupings = ['AGENT'],
        Metrics = [
            {
                'Name': 'AGENT_ANSWER_RATE'
            }
        ]
    )

    user_series =[]
    categories = []
    for user in user_data['MetricResults']:
        user_series.append(models.SeriesData(name = userDic[user['Dimensions']['AGENT']], 
                                              data=[round(user['Collections'][0]['Value'],3)]))
        categories.append(userDic[user['Dimensions']['AGENT']])

    user_xaxis = models.XAxisData(
        categories = categories
    )

    user_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = user_xaxis
    )

    user_chart = models.ChartData(
        type = "bar",
        series = user_series,
        options = user_options
    )

    user_graph = models.GenericGraph(
        title = "Agent Answer Rate",
        description = "This graph shows the answer rate of each agent.",
        footer = ("Updated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)),
        chart = user_chart
    )

    return user_graph
cachedData.add("queues_agent_answer_rate", queues_agent_answer_rate, 30)


async def queues_agent_occupancy():
    userNT = ["94c89e21-3aac-44b5-8ffa-c898061fddfd"]

    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    agentList = []
    agentDic = {}
    for user in users['UserSummaryList']:
        if user['Id'] not in userNT:
            agentList.append(user['Id'])
            agentDic[user['Id']] = user['Username']


    agent_data = client.get_metric_data_v2(
        # InstanceId = Config.INSTANCE_ID,
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e',
        StartTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [{
            'FilterKey': 'AGENT',
            'FilterValues': agentList,
        }],
        Groupings = ['AGENT'],
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY'
            }
        ]
    )

    agent_series =[]
    categories = []
    for agent in agent_data['MetricResults']:
        if 'Value' in agent['Collections'][0]:
            agent_series.append(models.SeriesData(name = agentDic[agent['Dimensions']['AGENT']], 
                                              data=[round(agent['Collections'][0]['Value'],3)]))
            categories.append(agentDic[agent['Dimensions']['AGENT']])

    agent_occ_xaxis = models.XAxisData(
        categories = categories
    )

    agent_options = models.GraphOptions(
        colors = ["#3b82f6", "#f87171"],
        xaxis = agent_occ_xaxis
    )

    agent_chart = models.ChartData(
        type = "bar",
        series = agent_series,
        options = agent_options
    )

    agent_occupancy_graph = models.GenericGraph(
        title = "Agent Occupancy of today",
        description = "This graph shows the answer rate of each agent.",
        footer = ("Updated at: " + str(datetime.now().hour) + ":" + str(datetime.now().minute)),
        chart = agent_chart
    )

    return agent_occupancy_graph

cachedData.add("queues_agent_occupancy", queues_agent_occupancy, 30)

async def get_current_user_data() -> dict:
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    users_data = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Agents': userList
        }
    )

    return users_data

cachedData.add('get_current_user_data', get_current_user_data, 30) # 30 seconds
