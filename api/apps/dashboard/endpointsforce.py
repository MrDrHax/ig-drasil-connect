# # ---------------------------------------------------- Volver a checar (requiere numero de telefono)
# @router.get("/get-current-metric-data")
# async def check_agent_availability(queue_id: str):
#     """
#     Description:
#         Real-time information of the call.
#     Parameters:
#         * InstanceId [REQUIRED][string]: id of the Amazon Connect instance.
#         * Filters [REQUIRED][dictionary]:  
#             - 

#     Read the docs:
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/get_current_metric_data.html#

#     @return 
#         Metrics about an on-going call.

#         ex. queue_id = '18494127-588c-4497-8291-9dacaee44341'
#     """    


#     client = boto3.client('connect')

#     # Get info for the first routing profile
#     response = client.get_current_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Queues': [queue_id],

#             'Channels': [
#                 'VOICE'
#             ]
#         },
#         CurrentMetrics=[
#         {
#             'Name': 'AGENTS_ONLINE',
#             'Unit': 'COUNT'
#         },
#         ]
#     )

#     return response['MetricResults']

#     # data = cachedData.get("check_agent_availability_data")

#     # return data
# # -------------------------------------------------Needs review
# # @router.get("/agent-status", response_model=List[dict])
# # async def check_agent_availability():
# #     """
# #     Description:
# #         Verifies the status of agents in Amazon Connect.
# #         It can be one of four things:

# #         * AVAILABLE: on-duty and not in call
# #         * OFFLINE: not on-duty and disconnected
# #         * BUSY: with an open thread or ongoing call
# #         * NEEDS ASSISTANCE: needs help from supervisor

# #     Parameters:
# #         * InstanceId [REQUIRED][string]: amazon connect instance identified
# #         * AgentStatusTypes [list]: The available agent status types
# #         * PaginationConfig [dictionary]
# #             * MaxItems [int]: total number of items to return
# #             * PageSize [int]: the size of each page
        
# #     Read the docs:
# #     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html

# #     @return 
# #         List containing the availability status of agents. (Not yet known)
# #     """

# #     client = boto3.client('connect')
# #     paginator = client.get_paginator('list_agent_statuses')

# #     # Get info for the first routing profile
# #     response_iterator = paginator.paginate(
# #         InstanceId = Config.INSTANCE_ID,
# #         AgentStatusTypes = [
# #             'AVAILABLE','OFFLINE','BUSY','ON BREAK','NEEDS ASSISTANCE',
# #         ])
    
# #     return response_iterator

# @router.get("/agent-profile", tags=["profile"])
# async def get_agent_profile(id: str) -> models.AgentProfileData:
#     '''
#     Returns the profile of an agent.

#     To get the full list, go to /lists/agents
#     '''
#     try:
#         client = boto3.client('connect')
#         response = client.describe_user(
#             InstanceId=Config.INSTANCE_ID,
#             UserId=id
#         )


#         FullName = f'{response["User"]["IdentityInfo"]["FirstName"]} {response["User"]["IdentityInfo"]["LastName"]}'
#         Agent_email = response["User"]["Username"]

#         try:
#             Agent_mobile = response["User"]["IdentityInfo"]["Mobile"]
#         except:
#             Agent_mobile = "Unknown"

#         # FullName, Agent_email, Agent_mobile = cachedData.get("agent_profile_data", id=id)

#         # logger.info(f"{FullName}, {Agent_email}, {Agent_mobile}")

#         return models.AgentProfileData(name=FullName, queue='Support', rating=4, email=Agent_email, mobile=Agent_mobile)

#     except Exception as e:
#         logger.error(f"Error in get_agent_profile: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

# # list_recommenders_cache = []

# # @router.get("/list-recommenders", response_model=List[dict])
# # async def list_recommenders():
# #     try:
# #         client = boto3.client('connect')
# #         response = client.list_queues(
# #             InstanceId='string',
# #             MaxResults=10
# #         )
        
# #         return response
# #     except Exception as e: 
# #         print(e.with_traceback)
# #         print(e)
        

# @router.get("/call-summary")
# async def call_summary():
#     """
#     Description:
#         Returns a series of metrics of a call with a certain contact specified by id

#     Parameters:
#         * InstanceId [REQUIRED][string]: amazon connect instance identified
#         * ContactId [REQUIRED][string]: identifier of the contact
        
#     Read the docs:
#     https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/client/describe_contact.html

#     @return 
#         JSON with the information on the call
#     """
#     try:
#         client = boto3.client('connect')
#         response = client.describe_contact(
#             InstanceId=Config.INSTANCE_ID,
#             ContactId='string'
#         )
        
#         return response
#     except Exception as e: 
#         print(e.with_traceback)
#         print(e)

# @router.get("/agent-status", response_model=List[dict])
# async def agent_status():
    
#     '''
#     Returns the agent status.
    
#     '''
    
#     client = boto3.client('connect')
#     response = client.list_agent_statuses(
#         InstanceId=Config.INSTANCE_ID
#     )
    
#     return response['AgentStatusSummaryList']    

# @router.get("/queue-description")
# async def queue_description(queue_id: str):
#     client = boto3.client('connect')
#     response = client.describe_queue(
#         InstanceId=Config.INSTANCE_ID,
#         QueueId=queue_id
#     )
    
#     return response['Queue']

# @router.get("/describe-routing-profile")
# async def describe_routing_profile(routing_profile_id: str):
#     client = boto3.client('connect')
#     response = client.describe_routing_profile(
#         InstanceId=Config.INSTANCE_ID,
#         RoutingProfileId=routing_profile_id
#     )
    
#     return response['RoutingProfile']


# @router.get("/list-routing-profile-queues")
# async def list_routing_profile_queues(routing_profile_id: str):
#     client = boto3.client('connect')

#     response = client.list_routing_profile_queues(
#         InstanceId=Config.INSTANCE_ID,
#         RoutingProfileId=routing_profile_id
#     )['RoutingProfileQueueConfigSummaryList']
    
#     return response

# @router.get("/describe-contact")
# async def describe_contact(contact_id: str):

#     client = boto3.client('connect')
#     response = client.describe_contact(
#         InstanceId=Config.INSTANCE_ID,
#         ContactId=contact_id
#     )

#     return response['Contact']

# # 802dc0a071714366b20b7dd891929556
# @router.get("/desciribe-user")
# async def describe_user(user_id:str):

#     client = boto3.client('connect')
#     response = client.describe_user(
#         InstanceId=Config.INSTANCE_ID,
#         UserId= user_id
#     )
#     return response['User']


# # @router.get("/get-transcript")
# # async def get_transcript(Contacd_Id: str, Connection_Token: str):

# #     client = boto3.client('connectparticipant')
# #     response = client.get_transcript(
# #         ContactId = Contacd_Id,
# #         ConnectionToken = request.cookies['access_token'], # Requerimos este token de autenticación.
# #     )
# #     return response['User']


# @router.get("/metric-data")
# async def metric_data(queue_id:str):

#     client = boto3.client('connect')
#     response = client.get_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         StartTime=datetime(2024, 5, 25, 0),
#         EndTime=datetime(2024, 5, 25, 16),
#         Filters={
#             'Queues': [
#                 queue_id
#                 ]
#         },
#         Groupings=[
#             'QUEUE'
#         ],
#         HistoricalMetrics=[
#             {
#                 'Name': 'INTERACTION_TIME',
#             # 'Threshold': {
#             #     'Comparison': 'LT',
#             #     'ThresholdValue': 123.0
#             # },
#                 'Statistic': 'AVG',
#                 'Unit': 'SECONDS'
#             },
#         ]
#     )

#     print(response)

#     return response['MetricResults']

# @router.get("/current-metric-data")
# async def current_metric_data(queue_id:str):

#     client = boto3.client('connect')
#     response = client.get_current_metric_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Queues': [
#                 queue_id
#             ],
#             'Channels': [
#                 'VOICE'
#             ]
#         },
#         Groupings=['QUEUE'],
#         CurrentMetrics=[
#         {
#             'Name': 'AGENTS_AVAILABLE',
#             'Unit': 'COUNT'
#         },
#         ]
#     )

#     print(response)

#     return response['MetricResults']


# @router.get("/current-user-data")
# async def get_current_user_data():

#     client = boto3.client('connect')
#     response = client.get_current_user_data(
#         InstanceId=Config.INSTANCE_ID,
#         Filters={
#             'Agents': [
#                 '1c38eb16-8f2c-4c9a-b723-8f0621583179',
#                 '270a9b75-7c3d-40de-b524-25011c6aeeb8',
#                 '305376be-597e-4c30-8cc1-d0ceb88699fe',
#                 '35eb516c-0c56-45a2-ab53-b09a43f196c3',
#                 '50f98823-5278-47fb-8c1a-e56fa525404a',
#                 '51ec1227-4119-412e-b0e6-2e3bbc6ae1a4',
#                 '7688a303-17b8-4402-b03f-d7ab051bde4e',
#                 '7d6be46a-287b-48fc-8bdb-70655a978247',
#                 '83656f24-be8f-4cc6-aca9-c3bf5c42e21a',
#                 '8d6f58c4-d1f5-4024-9ab0-c57666dd791b',
#                 '94c89e21-3aac-44b5-8ffa-c898061fddfd',
#                 'a3f8c7e6-712c-4c13-a9ae-5ed13e1f6523',                
#                 'b2ba1a5d-6f46-40a5-aa24-6b5032bf79fd',
#                 'ba862485-c72a-4fb9-8f98-58415b19482b',
#                 'c6437a67-db38-49da-8188-778ac2f1f555',
#                 'cf1410c7-01e9-484a-971a-e481924ee68e',
#                 'd2eed6e2-7bef-4983-83c8-cfd359d8cdbd',
#                 'fb1b7cb4-2e81-4d16-a50e-9726de5cc15a'
#             ],
#         #    'ContactFilter': {
#         #         'ContactStates': [
#         #             'CONNECTED'
#         #         ]
#         #     },
#         },
#         # CurrentMetrics=[
#         # {
#         #     'Name': 'AGENTS_AVAILABLE',
#         #     'Unit': 'COUNT'
#         # },
#         # ]
#     )

#     print(response)

#     return response['UserDataList']


# @router.get("/list-contacts")
# async def list_contacts():

#     client = boto3.client('connect')
#     response = client.search_contacts(
#         InstanceId=Config.INSTANCE_ID,
#         TimeRange={
#             'Type': 'INITIATION_TIMESTAMP',
#             # |'SCHEDULED_TIMESTAMP'|'CONNECTED_TO_AGENT_TIMESTAMP'|'DISCONNECT_TIMESTAMP',
#             'StartTime': datetime.today() - timedelta(days=56),
#             'EndTime': datetime.today(),
#         },
        
#         SearchCriteria={
#             'Channels': [
#                 'VOICE',
#             ],
#             'InitiationMethods': [
#                 'INBOUND',
#                 # |'OUTBOUND'|'TRANSFER'|'QUEUE_TRANSFER'|'CALLBACK'|'API'|'DISCONNECT'|'MONITOR'|'EXTERNAL_OUTBOUND',
#             ],
#         },

#         Sort={
#             'FieldName': 'INITIATION_TIMESTAMP',
#             # |'SCHEDULED_TIMESTAMP'|'CONNECTED_TO_AGENT_TIMESTAMP'|'DISCONNECT_TIMESTAMP'|'INITIATION_METHOD'|'CHANNEL',
#             'Order': 'ASCENDING'
#             # |'DESCENDING'
#         }
#     )

#     print(response)

#     return response['Contacts']