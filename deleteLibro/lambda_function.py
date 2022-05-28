import sys
import logging
import psycopg2
import json
import os

# rds settings
rds_host  = 'ypinilla-libros.cpppnoececan.us-east-1.rds.amazonaws.com'
rds_username = 'ypinilla'
rds_user_pwd = 'ypinilla123!'
rds_db_name = 'postgres'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn_string = "host=%s user=%s password=%s dbname=%s" % \
                    (rds_host, rds_username, rds_user_pwd, rds_db_name)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
except:
    logger.error("ERROR: Could not connect to Postgres instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")

def lambda_handler(event, context):

    isbn = event['isbn']

    query = """DELETE FROM libro
                WHERE isbn = %s returning 'Libro eliminado correctamente'"""

    query = query % (isbn)

    with conn.cursor() as cur:
        rows = []
        cur.execute(query)
        for row in cur:
            rows.append(row)

    return { 'statusCode': 200, 'body': rows }