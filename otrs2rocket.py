#!/usr/bin/python3
"""
 Post new OTRS tickets to Rocket.Chat channel

 Oliver Völker <info@ovtec.it>

 Modified by Nico Domino <ndomino@newtelco.de> for OTRS Postgres compatibility
"""

import pymysql
import psycopg2
import requests
import os
import sys

from dotenv import load_dotenv, find_dotenv
load_dotenv()

DEBUG = False

# Rocket.Chat incoming webhook URL
# prod:
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# dev:
#WEBHOOK_URL = os.getenv("WEBHOOK_URL_DEV")

# OTRS URL
OTRS_URL = os.getenv("OTRS_URL")

# MySQL settings
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_DB   = os.getenv("MYSQL_DB")

# PostgreSQL settings
PSQL_HOST = os.getenv("PSQL_HOST")
PSQL_PORT = int(os.getenv("PSQL_PORT"))
PSQL_USER = os.getenv("PSQL_USER")
PSQL_PASS = os.getenv("PSQL_PASS")
PSQL_DB   = os.getenv("PSQL_DB")

if len(sys.argv) < 3:
  print("CLI Arguments Missing")
  sys.exit (1)

if DEBUG:
  INPUT = {"1": sys.argv[1], "2": sys.argv[2]}
  print(INPUT,  file=open('/opt/otrs2rocket/out.log', 'a'))

if MYSQL_HOST:
  if DEBUG:
    print('mysql')
  conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB)
  cur = conn.cursor()
  sql = "SELECT ticket.id, ticket.tn, ticket.title, queue.name, CASE WHEN customer_company.name IS NOT NULL THEN customer_company.name ELSE ticket.customer_id END AS customer FROM ticket LEFT JOIN queue ON (ticket.queue_id = queue.id) LEFT JOIN customer_company ON (ticket.customer_id = customer_company.customer_id) WHERE tn = %s"
  cur.execute(sql, sys.argv[1])

if PSQL_HOST:
  if DEBUG:
    print('psql')
  conn = psycopg2.connect(dbname=PSQL_DB, user=PSQL_USER, password=PSQL_PASS, host=PSQL_HOST, port=PSQL_PORT)
  cur = conn.cursor()
  sql = "SELECT ticket.id, ticket.tn, ticket.title, queue.name, CASE WHEN customer_company.name IS NOT NULL THEN customer_company.name ELSE ticket.customer_id END AS customer FROM ticket LEFT JOIN queue ON (ticket.queue_id = queue.id) LEFT JOIN customer_company ON (ticket.customer_id = customer_company.customer_id) WHERE tn = %s"
  cur.execute(sql, (sys.argv[1],))

if cur.rowcount:
  for row in cur:
    id = str(row[0])
    tn = row[1]
    title = row[2]
    queue = row[3]
    customer = row[4]
else:
  # exit if no matching ticket was found
  cur.close()
  conn.close()
  print('Err: No matching ticket found!')
  sys.exit (0)

cur.close()
conn.close()

if DEBUG:
  print(cur.rowcount)
  print(id, tn, title, customer, queue)

headers = {'Content-type': 'application/json'}
payload = {'alias': 'OTRS Bot', 'icon_url': os.getenv("LOGO_URL"), 'text': '\n', 'attachments': [{ 'color': '#ab4a53', 'text': ':dna: ' + queue + '\n :bookmark_tabs: #' + tn + '\n :blond-haired_man_light_skin_tone: ' + customer + '\n\n :arrow_right: **' + title + '**\n\n:globe_with_meridians:  [View in OTRS](' + OTRS_URL + id + ')'}]}

if DEBUG:
  print(payload)

r = requests.post(WEBHOOK_URL, json=payload, headers=headers)

if DEBUG:
  print(r)

if r.status_code != 200:
  raise ValueError('Request to Rocket.Chat returned an error %s, the response is:\n%s' % (r.status_code, r.text))
