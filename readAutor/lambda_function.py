import sys
import logging
import pymysql
#rds settings
rds_host  = "ypinilla-autor.cpppnoececan.us-east-1.rds.amazonaws.com"
name = "ypinilla"
password = "ypinilla"
db_name = "ypinillaautor"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, name, password, db_name)

except:
    logger.error("ERROR: Could not connect to Mysql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS Mysql instance succeeded")

def lambda_handler(event, context):
    nombre = event.get('nombre', "")
    cedula = event['cedula'] or 0
    pais = event['pais'] or ""
    ciudad = event['ciudad'] or ""

    query = """SELECT * FROM autor
                WHERE nombre = %s OR cedula = %s OR pais = %s OR ciudad = %s"""

    query = query % (nombre, cedula, pais, ciudad)

    with conn.cursor() as cur:
        rows = []
        cur.execute(query)
        for row in cur:
            rows.append(row)
            conn.commit()
            cur.close()

    return { 'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': rows }