import itertools
import psycopg2
import sys
   # set threshold as a percent
   # (for example, 5% of Freecode baskets is about 2325)
MINSUPPORTPCT = 5

allSingletonTags = []
allDoubletonTags = set()
doubletonSet = set()


try:

                con = psycopg2.connect("dbname='association' user='whyteg'")

                cur = con.cursor()


                cur.execute("SELECT count(DISTINCT project_id) FROM fc_project_tags;")
                baskets  = cur.fetchall()
                intbasket = baskets[0][0]
                minsupport = intbasket * (MINSUPPORTPCT / 100)
                print("Minimum support count:", minsupport, "(", MINSUPPORTPCT, "% of", intbasket,")")

                cur.execute("SELECT DISTINCT tag_name FROM fc_project_tags "
                            "GROUP BY 1 HAVING COUNT(project_id) >= {} ORDER BY tag_name".format(minsupport))

                singletons = cur.fetchall()

                for (singleton) in singletons:
                    allSingletonTags.append(singleton[0])
                    print (singleton[0])


                # Doubletons
                # The use of itertools.combinations memory efficient processing
                doubletonCandidates = list(itertools.combinations(allSingletonTags, 2))
                #
                for (index, candidate) in enumerate(doubletonCandidates):
                    # figure out if this doubleton candidate is frequent
                    tag1 = candidate[0]
                    tag2 = candidate[1]
                    # cur.execute("SELECT count(fpt1.project_id) FROM fc_project_tags fpt1 INNER JOIN  fc_project_tags"
                    #             " fpt2 ON fpt1.project_id = fpt2.project_id WHERE fpt1.tag_name = {}"
                    #             " AND fpt2.tag_name = {}".format(tag1,tag2))


                    cur.execute("SELECT count(fpt1.project_id) \
                                      FROM fc_project_tags fpt1 \
                                      INNER JOIN fc_project_tags fpt2 \
                                      ON fpt1.project_id = fpt2.project_id \
                                      WHERE fpt1.tag_name = %s \
                                      AND fpt2.tag_name = %s", (tag1, tag2))

                    count = cur.fetchone()[0]
                    # count = cur.fetchall()

                    print (count)

                    if count > minsupport:
                        print(tag1, tag2, "[", count, "]")

                        cur.execute("INSERT INTO fc_project_tag_pairs \
                                               (tag1, tag2, num_projs) \
                                               VALUES (%s,%s,%s)", (tag1, tag2, count))

                        # save the frequent doubleton to our final list
                        doubletonSet.add(candidate)
                        # add terms to a set of all doubleton terms (no duplicates)
                        allDoubletonTags.add(tag1)
                        allDoubletonTags.add(tag2)


                # Tripletons
                tripletonCandidates = list(itertools.combinations(allDoubletonTags, 3))

                # sort each candidate tuple and add these to a new sorted candidate list
                tripletonCandidatesSorted = []
                for tc in tripletonCandidates:
                    tripletonCandidatesSorted.append(sorted(tc))

                    # figure out if this tripleton candidate is frequent
                    for (index, candidate) in enumerate(tripletonCandidatesSorted):
                        # all doubletons inside this tripleton candidate MUST also be frequent
                        doubletonsInsideTripleton = list(itertools.combinations(candidate, 2))

                        tripletonCandidateRejected = 0
                        for (index, doubleton) in enumerate(doubletonsInsideTripleton):
                            if doubleton not in doubletonSet:
                                tripletonCandidateRejected = 1
                                break
                        # add frequent tripleton to database
                        if tripletonCandidateRejected == 0:
                            cur.execute("SELECT count(fpt1.project_id) \
                                FROM fc_project_tags fpt1 \
                                INNER JOIN fc_project_tags fpt2 \
                                ON fpt1.project_id = fpt2.project_id \
                                INNER JOIN fc_project_tags fpt3 \
                                ON fpt2.project_id = fpt3.project_id \
                                WHERE (fpt1.tag_name = %s \
                                AND fpt2.tag_name = %s \
                                AND fpt3.tag_name = %s)", (candidate[0],
                                                           candidate[1],
                                                           candidate[2]))
                            count = cur.fetchone()[0]
                            if count > minsupport:
                                print(candidate[0], ",",
                                      candidate[1], ",",
                                      candidate[2],
                                      "[", count, "]")
                                cur.execute("INSERT INTO fc_project_tag_triples \
                                                (tag1, tag2, tag3, num_projs) \
                                                VALUES (%s,%s,%s,%s)",
                                               (candidate[0],
                                                candidate[1],
                                                candidate[2],
                                                count))


                con.commit()


except psycopg2.DatabaseError as e:
                print ('Error %s' % e)

finally:

                if con:
                    con.close()

                if cur:
                    cur.close()