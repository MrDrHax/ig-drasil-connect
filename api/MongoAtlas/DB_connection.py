
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure

#uri = "mongodb+srv://a01783155:hfVp8BtX7R9VblzG@igdrasildb.i4prhyj.mongodb.net/?retryWrites=true&w=majority&appName=IGDrasilDB"
uri = "mongodb+srv://a01783155:hfVp8BtX7R9VblzG@igdrasiltest.i4prhyj.mongodb.net/?retryWrites=true&w=majority&appName=IGDrasilTest"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     print(client.admin.command('ping'))
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)



"""
Singleton pattern 
"""



class DataBase:
    _instance = None

    def __init__(self):
        if DataBase._instance is not None:
            raise Exception("This class is a singleton!")
        try:
            #TODO Pasar el uri a .env, por lo que hay que crear una nueva
            self.client = MongoClient(uri,tls=True, tlsAllowInvalidCertificates=True) 
            self.db = self.client["IGDrasilTest"]  # OJO: cambiarlo por el nombre de la base de datos (creo David la tiene)
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            DataBase._instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DataBase()
        return cls._instance

    def get_database(self):
        return self.db
    
    def test_connection(self):
        try:
            # Verificar que la conexión es exitosa obteniendo la lista de colecciones
            collections = self.db.list_collection_names()
            print(collections)
            print("Connection successful! Collections:", collections)
            return True
        except Exception as e:
            print(f"Error during connection test: {e}")
            return False


if __name__ == "__main__":
    db_instance = DataBase.get_instance()
    db_instance.test_connection()