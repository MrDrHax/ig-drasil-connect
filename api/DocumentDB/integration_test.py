from pymongo import MongoClient
from ssh_pymongo import MongoSession
import sys

##Create the SSH tunnel
# session = MongoSession(
#     host='3.85.93.55',
#     user='ec2-user',
#     port=22,
#     key = 'ec2DocDB.pem',
#     uri = 'mongodb://Saikou17:JuanCarlos17!@docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&readPreference=secondaryPreferred&retryWrites=false',
#     # remote_bind_address=('docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com', 27017),
#     # local_bind_address=('')
# )
# session.start()

# db = session.connection['PruebaFuncionalidadMongo']

# col = db['Test1']

# col.insert_one({'hello':'Amazon DocumentDB'})

# db.list_collection_names()

# print(db.list_collection_names())

##Close the SSH tunnel
# session.stop()


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









#---------------------------------------------------
# Intento #3
from pymongo.errors import ConnectionFailure
import certifi

# Conexion al cliente
# ?tls=true&tlsCAFile=global-bundle.pem&readPreference=secondaryPreferred&retryWrites=false
# client = MongoClient('mongodb://Saikou17:JuanCarlos17!@docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com:27017/', tls = True, tlsCAFile='global-bundle.pem', tlsCertificateKeyFile = 'ec2DocDB.pem') 

# intente agregar esto:
# ssl=true&ssl_cert_reqs=CERT_NONE

try:
  print("certifi.where(): ", certifi.where())
  client = MongoClient('mongodb://Saikou17:JuanCarlos17!@docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com:27017/ssl=true&ssl_cert_reqs=CERT_NONE', tls = True, tlsCAFile= certifi.where(), tlsCertificateKeyFile = certifi.where()) 
  print("Connection to DocumentDB successful!")
  
  # Optional: Test a simple database operation (like getting server status)
  database = client["admin"]
  server_status = database.command("serverStatus")
  print(f"Server status: {server_status}")
  
except ConnectionFailure as e:
  print(f"Connection failed: {e}")
finally:
  if client:
    client.close()  # Close the connection

# Base de Datos:
# db = client['PruebaFuncionalidadMongo']
# Coleccion:
# col = db['Test1']

# Prueba de conexion:
# doc = {'JPmeLApela': 'Ahuevoooo se logro!!'}
# result = col.insert_one(doc)
# print('Document inserted:', result.inserted_id)