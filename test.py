from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["prueba3"]

print("Conectado a MongoDB")
print("Colecciones encontradas:")
print(db.list_collection_names())