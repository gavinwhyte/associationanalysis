import itertools
import psycopg2
import sys

X = 'Internet'
Y = 'Web'
try:

                con = psycopg2.connect("dbname='association' user='whyteg'")

                cursor = con.cursor()

                # grab basic counts from the database that we need
                numBasketsQuery = "SELECT count(DISTINCT project_id) \
                      FROM fc_project_tags"
                cursor.execute(numBasketsQuery)
                numBaskets = cursor.fetchone()[0]

                supportForXQuery = "SELECT count(*) \
                      FROM fc_project_tags \
                      WHERE (tag_name = {})"
                cursor.execute(supportForXQuery.format("'" + X + "'"))
                supportForX = cursor.fetchone()[0]

                print(supportForX)

except psycopg2.DatabaseError as e:
                print ('Error %s' % e)

finally:

                if con:
                    con.close()

                if cursor:
                    cursor.close()
