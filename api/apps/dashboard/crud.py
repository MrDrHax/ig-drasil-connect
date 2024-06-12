from sqlalchemy.orm import Session
from . import models
import boto3
from config import Config
from cache.cache_object import cachedData
from datetime import datetime , timedelta, date, timezone
import pytz
from tools.lazySquirrel import LazySquirrel

import logging
logger = logging.getLogger(__name__)

tz = pytz.timezone('America/Mexico_City')

async def agent_profile_data(id) -> tuple:
    client = boto3.client('connect')
    response = client.describe_user(
        InstanceId=Config.INSTANCE_ID,
        UserId=id
    )

    FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
    Agent_email = response["User"]["Username"]

    try:
        Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
    except:
        Agent_mobile = "Unknown"

    return FullName, Agent_email, Agent_mobile
cachedData.add("agent_profile_data", agent_profile_data, 60*60*24) # 24 hours

async def list_queue():
    """
    Returns a list of all queues that have the status "ENABLED".
    """
    client = boto3.client('connect')
    response = client.list_queues(
    InstanceId = Config.INSTANCE_ID,
    )

    ret = {'QueueSummaryList': []}
    for q in response['QueueSummaryList']:
        try:
            queue_data = await cachedData.get('get_queue_description', queueID=q['Id'])

            if queue_data['Status'] == 'ENABLED':
                ret['QueueSummaryList'].append(q)
        except:
            pass

    return ret
cachedData.add("list_queue", list_queue, 60 * 60 * 24) # 24 hours

async def list_routing_profile():
    client = boto3.client('connect')

    # Get a list of all routing profiles
    response = client.list_routing_profiles(
        InstanceId=Config.INSTANCE_ID
    )

    return response['RoutingProfileSummaryList']
cachedData.add("list_routing_profile", list_routing_profile, 60 * 60 * 24) # 24 hours

async def list_users():
    """
    Gets a list of all users that are active in the Connect instance.
    """
    client = boto3.client('connect')
    users = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )

    return users
cachedData.add("list_users", list_users, 30) # 30 seconds

async def online_users_data():
    client = boto3.client('connect')
    users = await cachedData.get("list_users")
    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )
    return response['UserDataList']
cachedData.add("online_users_data", online_users_data, 30)

async def get_not_connected_users_data():

    client = boto3.client('connect')
    users = await cachedData.get("list_users")

    userList = []
    for user in users['UserSummaryList']:
        userList.append(user['Id'])

    response = client.get_current_user_data(
        InstanceId=Config.INSTANCE_ID,
        Filters={
            'Agents': userList
        }
    )

    for user in response['UserDataList']:
        if user['User']['Id'] in userList:
            userList.remove(user['User']['Id'])

    return userList
cachedData.add("get_not_connected_users_data", get_not_connected_users_data, 30)

async def get_avg_call_time():
    routing_profile_list = await cachedData.get("list_routing_profile")
    client = boto3.client('connect')
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION',
            }
        ]
        
    
    )

    data=response['MetricResults'][0]['Collections'][0]['Value']

    cardFooter = models.CardFooter(
        color ="text-green-500",
        value="",
        label="The average duration of a contact in minutes this month"
    )

    card = models.GenericCard(
        id=1,
        title="Average Call Time",
        value="{p:.2f}".format(p=data/60),
        icon="Clock",
        footer=cardFooter,
        color="blue"
    )

    return card
cachedData.add("get_avg_call_time", get_avg_call_time, 60 * 60 * 24) # 24 hours
 
async def get_avg_contact_duration():
    client = boto3.client('connect')

    routing_profile_list = await cachedData.get("list_routing_profile")
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            # Here we need to pass a list of routing profiles that we get from another endpoint
            'FilterValues' : [i['Id'] for i in routing_profile_list],
            } 
        ],
        
        Metrics = [
            {
                'Name': 'AVG_CONTACT_DURATION'
            },
            {
                'Name': 'ABANDONMENT_RATE'
            }
        ]
        
    
    )

    #We need to get the timestamps for the x axis
    timestamps = []

    #We need to get the data for the y axis points
    data = []

    for j in range(len(response['MetricResults'])):
        # Save the timestamps in a list
        timestamps.append(response['MetricResults'][j]['MetricInterval']['StartTime'].strftime('%Y-%m-%d'))
        # Save the data in a list when the name is AVG_CONTACT_DURATION
        data.append(response['MetricResults'][j]['Collections'][0]['Value']) 

    # Create the graph points
    series_example = [models.SeriesData(name=response['MetricResults'][0]['Collections'][0]['Metric']['Name'], data=data)]

    # Create the x axis labels
    xaxis_example = models.XAxisData(
        categories=timestamps
    )

    # Create the graph options
    example_options = models.GraphOptions(
        xaxis=xaxis_example
    )

    # Create the graph type
    example_chart = models.ChartData(
        type="line",
        series= series_example,
        options=example_options
    )

    # Create the graph
    example_graph = models.GenericGraph(
        title="Average Contact Duration",
        description="Graph showing average contact duration per day in seconds",
        footer="Updated " + datetime.today().strftime('%Y-%m-%d'),
        chart = example_chart
    )

    return example_graph
cachedData.add("get_avg_contact_duration", get_avg_contact_duration, 60 * 60 * 24) # 24 hours

# THIS FUNCTION IS NOT BEING CALLED
async def get_connected_agents():
    client = boto3.client('connect')

    StartTime =  datetime((date.today() - timedelta(days=31)).year,
                          (date.today() - timedelta(days=31)).month, 1)
                                   
    EndTime =  datetime((date.today() - timedelta(days=31)).year, 
                                (date.today() - timedelta(days=31)).month, 
                                (datetime(date.today().year, date.today().month, 1) - timedelta(days=1)).day,
                                23, 59, 59)
    
    past_month_res = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'INITIATION_TIMESTAMP',
            'StartTime': StartTime,                                  
            'EndTime': EndTime,
        },
        
        SearchCriteria={
            'Channels': [
                'VOICE',
            ],
            'InitiationMethods': [
                'INBOUND',
            ],
        },

        Sort={
            'FieldName': 'INITIATION_TIMESTAMP',
            'Order': 'ASCENDING'
        }
    )

    today_res = client.search_contacts(
        InstanceId=Config.INSTANCE_ID,
        TimeRange={
            'Type': 'INITIATION_TIMESTAMP',
            'StartTime': datetime(datetime.now().year, datetime.now().month, datetime.now().day),
            'EndTime': datetime.now(),
        },
        
        SearchCriteria={
            'Channels': [
                'VOICE',
            ],
            'InitiationMethods': [
                'INBOUND',
            ],
        },

        Sort={
            'FieldName': 'INITIATION_TIMESTAMP',
            'Order': 'ASCENDING'
        }
    )

    past_month_AVG = round(past_month_res['TotalCount']/30)
    
    footer_info = models.CardFooter(color = "text-red-500" if today_res['TotalCount'] <= past_month_AVG else "text-green-500", 
                                    value=(str(today_res['TotalCount'] - past_month_AVG) if today_res['TotalCount'] <= past_month_AVG else ("+" + str(today_res['TotalCount'] - past_month_AVG))), 
                                    label= "than last month's average")
    card= models.GenericCard(
        id=1,
        title="Connected users",
        value=str(today_res['TotalCount']),
        icon="UserIcon",
        footer=footer_info
    )
    return card
cachedData.add("get_connected_agents", get_connected_agents, 60)

async def get_capacity():
    client = boto3.client('connect')

    routing_profile_list = await cachedData.get("list_routing_profile") 
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    response2 = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'ROUTING_PROFILE',
            'FilterValues' : [i['Id'] for i in routing_profile_list],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    datares1 = []
    for i in response['MetricResults']:
        for n in i['Collections']:
            datares1.append(n['Value'])
    
    datares2 = []
    for i in response2['MetricResults']:
        for n in i['Collections']:
            datares2.append(n['Value'])


    comp = datares1[0]-datares2[0]

    cardFooter = models.CardFooter(
        color = "text-red-500" if comp > 0 else "text-green-500",
        value = "{p:.2f}".format(p=comp),
        label ="more than last month" if comp > 0 else "less than last month"
    )
    
    card = models.GenericCard(
        id = 1,
        title = "Percentage of time \t  active agents",
        value = "{p:.2f}".format(p=datares1[0]),
        icon = "Person",
        footer = cardFooter
    )

    
    
    return card
cachedData.add("get_capacity", get_capacity, 60)

async def get_abandonment_rate():
    #routing_profile_list = await routing_profiles()
    #routing_profile_list = await routing_profiles()
    client = boto3.client('connect')

    queues_list = await cachedData.get("list_queue")

    queues_id_list = []    
    for i in queues_list['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_id_list.append(i['Id'])
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'QUEUE',
            'FilterValues' : queues_id_list,  
            } 
        ],
        Groupings=['QUEUE'],
        Metrics = [
            {
                'Name': 'ABANDONMENT_RATE',
            }
        ]
    )

    card_values = [i['Collections'][0]['Value'] for i in response['MetricResults']]
    card_value = sum(card_values) / len(card_values)

    if (card_value > 80):
        footerColor = "text-red-500"
        footerSpecialText = f'{card_value - 80:.2f}%'
        footerDesc = 'more than the max recommended rate.'
    elif (card_value > 50):
        footerColor = "text-orange-500"
        footerSpecialText = f'{card_value - 50:.2f}%'
        footerDesc = 'more than the recommended rate.'
    else:
        footerColor = "text-green-500"
        footerSpecialText = f'{0}%'
        footerDesc = 'more than the max recommended rate.'

    cardFooter = models.CardFooter(
        color=footerColor,
        value=footerSpecialText,
        label=footerDesc + " The abandonment rate is the amount of calls that where ended by the user before having contact with an agent.",
    )

    card = models.GenericCard(
        id=1,
        title="Abandonment rate",
        value="{:.2f}%".format(card_value),
        icon="Phone",
        footer=cardFooter,
    )
    
    return card
cachedData.add("get_abandonment_rate", get_abandonment_rate, 60)

async def get_connected_users():
    
    data = await cachedData.get('routing_profiles_data')

    totalAgents = len(data)
    agentsInCall = len(LazySquirrel(data).filter_by('status', 'on call').get())
    agentsWhoNeedHelp = len(LazySquirrel(data).filter_by('status', 'needs assistance').get())
    
    footer_info = models.CardFooter(
        color = "text-red-500" if agentsWhoNeedHelp > 0 else "text-green-500", 
        value= f"{agentsWhoNeedHelp} agents", 
        label= "need help. Get more details on the agents tab.")
    
    card= models.GenericCard(
        id=1,
        title="Agents in call.",
        value=f'{agentsInCall} out of {totalAgents} connected agents',
        icon="PhoneArrow",
        footer=footer_info,
        color="pink",
    )
    return card
cachedData.add("get_connected_users", get_connected_users, 60)

async def get_queues():
    client = boto3.client('connect')   

    queues_raw = await cachedData.get("list_queue")

    queues_list = []    
    
    for i in queues_raw['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_list.append([i['Id'], i['Name']])

    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Queues' : [i[0] for i in queues_list],
        },
        Groupings=['QUEUE',],
        CurrentMetrics = [
            {
                'Name': 'CONTACTS_IN_QUEUE', 
                'Unit': 'COUNT'
            }
        ],
    )

    data = []

    for j in response['MetricResults']:
        data.append(j['Collections'][0]['Value']) 
    
    series_example = [models.SeriesData(name=response['MetricResults'][0]['Collections'][0]['Metric']['Name'], data=data)]

    # Create the x axis labels
    xaxis_example = models.XAxisData(
        categories=[i[1] for i in queues_list]
    )

    # Create the graph options
    example_options = models.GraphOptions(
        xaxis=xaxis_example
    )

    # Create the graph type
    example_chart = models.ChartData(
        type="bar",
        series= series_example,
        options=example_options
    )

    # Create the graph
    example_graph = models.GenericGraph(
        title="Queues",
        description="Graph shows capacity the all queues",
        footer="Updated " + datetime.today().strftime('%Y-%m-%d') ,
        chart = example_chart
    )

    return example_graph
cachedData.add("get_queues", get_queues, 60)

# Agent Dashboard

async def last_month_avg_holds(agent_id):
    StartTime =  datetime((date.today() - timedelta(days=31)).year,
                          (date.today() - timedelta(days=31)).month, 1)
                                   
    EndTime =  datetime((date.today() - timedelta(days=31)).year, 
                                (date.today() - timedelta(days=31)).month, 
                                (datetime(date.today().year, date.today().month, 1) - timedelta(days=1)).day,
                                23, 59, 59)
    
    client = boto3.client('connect')

    past_month_res = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = StartTime,
        EndTime = EndTime,
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AVG_HOLDS',
            }
        ]
    )

    past_month_data = []
    for i in past_month_res['MetricResults']:
        for n in i['Collections']:
            past_month_data.append(n['Value'])

    return past_month_data
cachedData.add("last_month_avg_holds", last_month_avg_holds, 60 * 60 * 24) # 24 hours

async def get_avg_holds(agent_id):
    client = boto3.client('connect')
    
    queues_list = await cachedData.get("list_queue")

    queues_id_list = []    
    for i in queues_list['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_id_list.append(i['Id'])    
    
    today_res = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime(datetime.now().year, datetime.now().month, datetime.now().day),
        EndTime = datetime.now(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'DAY',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AVG_HOLDS',
            }
        ]
    )

    today_data = []
    for i in today_res['MetricResults']:
        for n in i['Collections']:
            today_data.append(n['Value'])

    past_month_data = await cachedData.get("last_month_avg_holds", agent_id=agent_id)

    if len(today_data) == 0 or len(past_month_data) == 0:
        #Return an empty card in case of no data
        return models.GenericCard(
            id=1,
            title="Average Holds",
            value="0",
            icon="Clock",
            footer= models.CardFooter(
                color="text-green-500",
                value="You have no holds.",
                label="Great job!",
            )
        )

    cardFooter = models.CardFooter(
        color="text-red-500" if today_data[0] > past_month_data[0] else "text-green-500",
        value=(str(today_data[0] - past_month_data[0]) if  today_data[0] <= past_month_data[0] else ("+" + str(today_data[0] - past_month_data[0]))),
        label=" times more today per contact than last month" if today_data[0] <= past_month_data[0] else " times less today per contact than last month",
    )

    card = models.GenericCard(
        id=1,
        title="Average customer hold time",
        value=str(today_data[0]),# Ensure this is a string
        icon="Clock",
        footer=cardFooter,
    )

    return card
cachedData.add("get_avg_holds", get_avg_holds, 60) # 60 seconds

async def get_People_to_answer():
    client = boto3.client('connect')
    
    queues_raw = await cachedData.get("list_queue")

    queues_list = []    
    
    for i in queues_raw['QueueSummaryList']:
        if i['QueueType'] == 'STANDARD':
            queues_list.append([i['Id'], i['Name']])

    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'Queues' : [i[0] for i in queues_list],
        },
        Groupings=['QUEUE',],
        CurrentMetrics = [
            {
                'Name': 'CONTACTS_IN_QUEUE', 
                'Unit': 'COUNT'
            }
        ],
    )

    data=0
    
    for i in response['MetricResults']:
        for n in i['Collections']:
            data += n['Value']
    
    cardFooter = models.CardFooter(
        color="text-red-500" if data.__round__() > 5 else "text-green-500",
        value=str(data.__round__()),
        label="are waiting to be answered. " + ("Hurry up, make sure to finish this call as fast as possible." if data.__round__() > 5 else "You are doing a great job, keep it up!"),
    )

    card = models.GenericCard(
        id=1,
        title="People waiting to be answered",
        # Get just the integer value from data
        value= str(data.__round__()), 
        icon="Person",
        footer=cardFooter,
        color="green"
    )

    return card
cachedData.add("get_People_to_answer", get_People_to_answer, 60) # 60 seconds

async def past_month_capacity_agent(agent_id):
    client = boto3.client('connect')

    response2 = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today() - timedelta(days=30),
        EndTime = datetime.today(),
        Interval = {
            'TimeZone': 'UTC',
            'IntervalPeriod': 'TOTAL',
        },
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    return response2
cachedData.add("past_month_capacity_agent", past_month_capacity_agent, 60 * 60 * 24) # 24 hours

async def get_capacity_agent(agent_id):
    client = boto3.client('connect')
    
    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [agent_id],  
            } 
        ], 
        Metrics = [
            {
                'Name': 'AGENT_OCCUPANCY',
            }
        ]
    )

    response2 = await cachedData.get('past_month_capacity_agent', agent_id=agent_id)

    try:
        
        datares1 = []
        for i in response['MetricResults']:
            for n in i['Collections']:
                datares1.append(n['Value'])
        
        datares2 = []
        for i in response2['MetricResults']:
            for n in i['Collections']:
                datares2.append(n['Value'])

        comp = datares1[0]-datares2[0]

        cardFooter = models.CardFooter(
            color = "text-red-500" if comp > 0 else "text-green-500",
            value = "{p:.2f}%".format(p=comp),
            label ="more than last month" if comp > 0 else "less than last month. To get it up, take as much calls as possible!"
        )
        
        card = models.GenericCard(
            id = 1,
            title = "Percentage of active time",
            value =  "{p:.2f}%".format(p=datares1[0]),
            icon = "Chart",
            footer = cardFooter,
            color="blue"
        )

    # If there is no data for the agent return no data
    except:
        card = models.GenericCard(
            id = 0,
            title = "Percentage of active time",
            value =  "No data",
            icon = "Chart",
            footer = models.CardFooter(
                color = "text-red-500",
                value = "",
                label ="No data"
            ),
            color="blue"
        )
    
    return card
cachedData.add("get_capacity_agent", get_capacity_agent, 60)

# Other endpoints

async def list_users_data():
    client = boto3.client('connect')

    # Get info about the users of said instance
    response = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )

    return response['UserSummaryList']
cachedData.add("list_users_data", list_users_data, 60)

async def get_usename(agent_id):
    client = boto3.client('connect')
    # Get info about the users of said instance
    response = client.list_users(
        InstanceId=Config.INSTANCE_ID,
    )
    for i in response['UserSummaryList']:
        if i['Id'] == agent_id:
            return i['Username']
cachedData.add("get_usename", get_usename, 60)

#------ Alerts endpoints

async def get_alert_supervisor_NA():
    data = await cachedData.get("routing_profiles_data") 

    agentNeedsAssistance = 0
    
    for i in data:
        if i['status'] == "Needs Assistance":
            agentNeedsAssistance += 1

    if agentNeedsAssistance > 0:
        alert = models.GenericAlert(
            Text="You have "+str(agentNeedsAssistance) +  " agents who need your help. ",
            TextRecommendation="You should go a Queue and see who needs help and go to the agent who needs help.",
            color="red",
            timestamp= datetime.now(tz).strftime('%Y-%m-%d %H:%M')
        )
        return alert
    return None
cachedData.add("get_alert_supervisor_NA", get_alert_supervisor_NA, 60)

async def get_alert_supervisor_available():
    client = boto3.client('connect')
    routing_profile_list = await cachedData.get("list_routing_profile")

    response = client.get_current_metric_data(
        InstanceId=Config.INSTANCE_ID,
        Filters = {
            'RoutingProfiles':[i['Id'] for i in routing_profile_list],
        },
        Groupings=['QUEUE',],

        CurrentMetrics = [
            {
                'Name': 'AGENTS_AVAILABLE', 
                'Unit': 'COUNT'
            }
        ],
    )

    data = 0
    for i in response['MetricResults']:
        for n in i['Collections']:
            data += n['Value']

    if data == 0:
        alert = models.GenericAlert(
            Text="There are no agents available.",
            TextRecommendation=" You should check first to see if your agents are busy or offline to see if any of them might be available again.",
            color="red",
            timestamp= datetime.now(tz)
        )
        return alert
    else:
        alert = models.GenericAlert(
            Text="There are "+ str(round(data)) + " agents available.",
            TextRecommendation="You should check first to see if your agents are busy or offline to see if any of them might be available again.",
            color="green",
            timestamp= datetime.now(tz).strftime('%Y-%m-%d %H:%M')
        )
        return alert
cachedData.add("get_alert_supervisor_available", get_alert_supervisor_available, 60)

async def get_alert_supervisor_nonResponse():
    client = boto3.client('connect')
    agent= await list_users_data()

    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : [i['Id'] for i in agent],  
            } 
        ], 

        Groupings=['AGENT', ],

        Metrics = [
            {
                'Name': 'AGENT_NON_RESPONSE_WITHOUT_CUSTOMER_ABANDONS',
            }
        ]
    )
    
    alert = []

    for i in response['MetricResults']:
        for n in i['Collections']:
            if n['Value'] > 0:
                alert.append(models.GenericAlert(
                    Text="Agent "+ await get_usename(i["Dimensions"]["AGENT"]) + " has not responded during the call with the client.",
                    TextRecommendation="You could intervene in the call or send him a message as to why he is silent in front of the customer",
                    color="red",
                    timestamp= datetime.now(tz).strftime('%Y-%m-%d %H:%M')
                ))
    return alert
cachedData.add("get_alert_supervisor_nonResponse", get_alert_supervisor_nonResponse, 60)

async def get_alert_agent_nonResponse(agent_id):
    client = boto3.client('connect')
    agent= await list_users_data()

    response = client.get_metric_data_v2(
        ResourceArn = 'arn:aws:connect:us-east-1:654654498666:instance/433f1d30-6d7d-4e6a-a8b0-120544c8724e' ,
        StartTime = datetime.today()-timedelta(days=1),
        EndTime = datetime.today(),
        Filters = [
            {
            'FilterKey': 'AGENT',
            'FilterValues' : agent_id,  
            } 
        ], 

        Groupings=['AGENT', ],

        Metrics = [
            {
                'Name': 'AGENT_NON_RESPONSE_WITHOUT_CUSTOMER_ABANDONS',
            }
        ]
    )
    data = response['MetricResults'][0]['Collections'][0]['Value']
    if data > 0:
        alert = models.GenericAlert(
            Text="You have not responded during the call with the client.",
            TextRecommendation="You could ask for help from a supervisor or ask the client if he has any questions.",
            color="orange",
            timestamp= datetime.now(tz).strftime('%Y-%m-%d %H:%M')
        )
        
    return alert
cachedData.add("get_alert_agent_nonResponse", get_alert_agent_nonResponse, 60)
