import itertools
import psycopg2
import sys
import datetime


   # set threshold as a percent
   # (for example, 5% of Freecode baskets is about 2325)


def generateRules():
    print("======")
    print("Association Rules:")
    print("======")

    # pull final list of tripletons to make the rules
    cur.execute("SELECT tag1, tag2, tag3, num_projs FROM fc_project_tag_triples")
    triples = cur.fetchall()
    for (triple) in triples:
        tag1 = triple[0]
        tag2 = triple[1]
        tag3 = triple[2]
        ruleSupport = triple[3]

        calcSCAV(tag1, tag2, tag3, ruleSupport)
        calcSCAV(tag1, tag3, tag2, ruleSupport)
        calcSCAV(tag2, tag3, tag1, ruleSupport)
        print("*")


def calcSCAV(tagA, tagB, tagC, ruleSupport):
    # Support
    ruleSupportPct = round((ruleSupport / baskets), 2)

    # Confidence
    query1 = "SELECT num_projs FROM fc_project_tag_pairs \
            WHERE (tag1 = %s AND tag2 = %s) or (tag2 = %s AND tag1 = %s)"
    cur.execute(query1, (tagA, tagB, tagB, tagA))
    pairSupport = cur.fetchone()[0]
    confidence = round((ruleSupport / pairSupport), 2)

    # Added Value
    query2 = "SELECT count(*) FROM fc_project_tags WHERE tag_name= {}"
    cur.execute(query2.format("'" + tagC + "'"))
    supportTagC = cur.fetchone()[0]
    supportTagCPct = supportTagC / baskets
    addedValue = round((confidence - supportTagCPct), 2)

    # Result
    print(tagA, ",", tagB, "->", tagC,
          "[S=", ruleSupportPct,
          ", C=", confidence,
          ", AV=", addedValue,
          "]")


try:

                con = psycopg2.connect("dbname='association' user='whyteg'")

                cur = con.cursor()

                queryBaskets = 'SELECT * FROM patrec limit 100;'

                cur.execute(queryBaskets)

                baskets = cur.fetchall()

                # generateRules()

                #
                for basket in baskets:
                     dt1 = datetime.datetime.strptime(str(int(basket[3])), '%Y%m%d%H%M%S')
                     dt2 = datetime.datetime.strptime(str(int(basket[12])), '%Y%m%d%H%M%S')
                     print(dt1)
                     print(dt2)
                #     # update the date column





except psycopg2.DatabaseError as e:
                print ('Error %s' % e)

finally:

                if con:
                    con.close()

                if cur:
                    cur