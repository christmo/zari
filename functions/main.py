import sqlalchemy
import os
import json
from telegram import impl as telegram
from general import impl as general

def init_connection_engine():
    db_config = {
        # [START cloud_sql_postgres_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_postgres_sqlalchemy_limit]

        # [START cloud_sql_postgres_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_postgres_sqlalchemy_backoff]

        # [START cloud_sql_postgres_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_postgres_sqlalchemy_timeout]

        # [START cloud_sql_postgres_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_postgres_sqlalchemy_lifetime]
    }
    print(os.environ.get("DB_HOST"))
    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        #return init_unix_connection_engine(db_config)
        return None

def init_tcp_connection_engine(db_config):
    # [START cloud_sql_postgres_sqlalchemy_create_tcp]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name  # e.g. "my-database-name"
        ),
        **db_config
    )
    # [END cloud_sql_postgres_sqlalchemy_create_tcp]
    pool.dialect.description_encoding = None
    return pool

def respuesta(message):
    text = []
    text.append(message)

    text_wrapper = {}
    text_wrapper["text"] = text

    fullfillment = []
    fullfillment_message = {}
    fullfillment_message["text"] = text_wrapper
    fullfillment.append(fullfillment_message)

    response = {}
    response["fulfillmentMessages"] = fullfillment
    return json.dumps(response)

def zari_webhook(request):
    """
        Entrada del Webhook de Dialogflow, en este se van a enviar los parametros
        a las otras funciones para realizar las acciones de respuesta.
    """
    text = ""
    request_json = request.get_json()
    print(request_json)
    if request_json != None and request_json["queryResult"] != None and request_json["originalDetectIntentRequest"] != None:
        #text = request_json["queryResult"]["queryText"]
        source = request_json["originalDetectIntentRequest"]["source"]
        if source == "telegram":
            text = telegram.gateway(request_json)
        else:
            text = general.gateway(request_json)
    else:
        text = "Respuesta sin procesar"
        db = init_connection_engine()
        with db.connect() as conn:
            usuarios = conn.execute(
                "SELECT * FROM usuarios "
            ).fetchall()
            for usuario in usuarios:
                print(usuario)

    return respuesta(text)
