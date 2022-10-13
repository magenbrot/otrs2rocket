#!/usr/bin/python3
#
# Post new OTRS tickets to Rocket.Chat channel
#
# Oliver Völker <info@ovtec.it>
#

import os
import pymysql
import requests
import sys

# Rocket.Chat incoming webhook URL
#
# prod:
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# test:
#WEBHOOK_URL = os.getenv("WEBHOOK_URL_DEV")

# OTRS URL
OTRS_URL = os.getenv("OTRS_URL")

# MySQL settings
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_DB   = os.getenv("MYSQL_DB")

if len(sys.argv) < 3:
    print("too less arguments")
    sys.exit (1)

conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB)
cur = conn.cursor()
sql = "SELECT ticket.id, ticket.tn, ticket.title, queue.name, CASE WHEN customer_company.name IS NOT NULL THEN customer_company.name ELSE ticket.customer_id END AS customer FROM ticket LEFT JOIN queue ON (ticket.queue_id = queue.id) LEFT JOIN customer_company ON (ticket.customer_id = customer_company.customer_id) WHERE tn = %s"
cur.execute(sql, sys.argv[1])

#print(cur.description)
#print()

if cur.rowcount:
    for row in cur:
      #print(row)
      id = str(row[0])
      tn = row[1]
      title = row[2]
      customer = row[3]
      queue = row[4]
else:
    # exit if no matching ticket was found
    cur.close()
    conn.close()
    sys.exit (0)

cur.close()
conn.close()

headers = {'Content-type': 'application/json'}
payload = {'text': 'New ticket #' + tn + ' in queue \"' + queue + '\" from \"' + customer + '\" --> \"' + title + '\"\n' + OTRS_URL + id}
#print(payload)
r = requests.post(WEBHOOK_URL, json=payload, headers=headers)

if r.status_code != 200:
    raise ValueError('Request to Rocket.Chat returned an error %s, the response is:\n%s' % (r.status_code, r.text))
