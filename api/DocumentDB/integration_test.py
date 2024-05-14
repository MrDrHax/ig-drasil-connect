import pymongo
from ssh_pymongo import MongoSession
import sys

##Create the SSH tunnel
session = MongoSession(
    host='3.85.93.55',
    user='ec2-user',
    port=22,
    key = 'ec2DocDB.pem',
    uri = 'mongodb://Saikou17:JuanCarlos17!@docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&readPreference=secondaryPreferred&retryWrites=false',
    # remote_bind_address=('docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com', 27017),
    # local_bind_address=('')
)
session.start()

db = session.connection['PruebaFuncionalidadMongo']

# col = db['Test1']

# col.insert_one({'hello':'Amazon DocumentDB'})

# db.list_collection_names()

print(db.list_collection_names())

##Close the SSH tunnel
session.stop()


##Create a MongoDB client, open a connection to Amazon DocumentDB as a replica set and specify the read preference as secondary preferred

# client = pymongo.MongoClient('mongodb://Saikou17:JuanCarlos17!@docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&readPreference=secondaryPreferred&retryWrites=false') 





# ##Specify the database to be used
# db = client.PruebaFuncionalidadMongo

# ##Specify the collection to be used
# col = db.Test1

# ##Insert a single document
# col.insert_one({'hello':'Amazon DocumentDB'})

# ##Find the document that was previously written
# x = col.find_one({'hello':'Amazon DocumentDB'})

# ##Print the result to the screen
# print(x)

# ##Close the connection
# client.close()
