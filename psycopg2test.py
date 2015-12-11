import psycopg2
from psycopg2 import extras
import json

#connection = psycopg2.connect("dbname=test user=gretchen")

#cursor = connection.cursor()

def get_user_info(request, all_params):
	print(request)
	for param in all_params:
		n=0
		print param + ': ' + all_params[param]
		n = n+1
	userid = 127
	username = 'kdf'

	try:
		conn = psycopg2.connect("dbname='northbridgedb' user='Gretchen' host='localhost' ")
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cur.execute("""SELECT * FROM forum_user""")
		#cur.execute("""SELECT * FROM forum_user WHERE id = %s AND username = %s""", (userid, username,))
		rec = cur.fetchall()
		jsonarray = json.dumps(rec)
		print(jsonarray)

	
	except:
		print("I am unable to connect to the database")

	
