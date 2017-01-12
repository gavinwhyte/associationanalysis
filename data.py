
import psycopg2
import sys

fd = open('tags.sql', 'r')
sqlFile = fd.read()
fd.close()

sqlCommands = sqlFile.split(';')

try:

                con = psycopg2.connect("dbname='association' user='whyteg'")

                cur = con.cursor()

                # for command in sqlCommands:
                #     print(len(command))
                #     if len(command) > 2:
                #         cur.execute(command)

                cur.execute("SELECT Count(*)  FROM fc_project_tags")
                rows = cur.fetchall()
                # #
                for row in rows:
                   print(row)
                print ("Done")
                con.commit()
except psycopg2.DatabaseError as e:
                print ('Error %s' % e)


finally:

                if con:
                    cur.close()
                    con.close()