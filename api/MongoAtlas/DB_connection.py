from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config

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
            self.client = MongoClient(Config.URI_MONGODB, tls=True, tlsAllowInvalidCertificates=True) 
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