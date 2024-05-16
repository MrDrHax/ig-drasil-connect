from sshtunnel import SSHTunnelForwarder
import sys, os, ssl, pymongo

# Ruta al archivo de certificado CA
CA_FILE_PATH = "global-bundle.pem"

# Verifica que el archivo CA exista
if not os.path.exists(CA_FILE_PATH):
    raise FileNotFoundError(f"CA file not found: {CA_FILE_PATH}")

##Create the SSH tunnel
server = SSHTunnelForwarder(
    ("3.85.93.55",22),
    ssh_username = "ec2-user",
    ssh_pkey = "ec2DocDB.pem",
    remote_bind_address=('docdb-2024-05-08-03-57-39.cluster-cn6o4mmauqhn.us-east-1.docdb.amazonaws.com',27017),
    local_bind_address= ('localhost',27017)
)

##We turn on the server with the ssh tunnrl
server.start()

try:
    # Iniciar el túnel SSH
    server.start()
    print("SSH Tunnel established")

    # Crear el cliente MongoDB a través del túnel
    client = pymongo.MongoClient(
        'mongodb://localhost:27017/?tls=true&tlsAllowInvalidHostnames=true&tlsCAFile=global-bundle.pem&readPreference=secondaryPreferred&retryWrites=false'
    )

    # Intentar acceder a la base de datos 'admin' y obtener información del servidor
    db = client['admin']
    server_info = db.command("serverStatus")
    print("Successfully connected to DocumentDB through SSH Tunnel.")
    print("Server Info:", server_info)

except Exception as e:
    print("Error:", e)

finally:
    # Detener el túnel SSH
    server.stop()
    print("SSH Tunnel stopped")