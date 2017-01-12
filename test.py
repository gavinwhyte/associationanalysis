
import psycopg2
import sys

try:

    con = psycopg2.connect("dbname='association' user='whyteg'")

    cur = con.cursor()
    cur.execute("SELECT * FROM fc_project_tags")

    rows = cur.fetchall()

    for row in rows:
        print
        row


except psycopg2.DatabaseError as e:
    print ('Error %s' % e)


finally:

    if con:
        con.close()