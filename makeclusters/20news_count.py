import os
import re, string

direc = "20news-18828"

def query_ordinal(ord):
    count = 0
    for dirname, dirnames, filenames in os.walk(direc):
        for idx, filename in enumerate(filenames):
            count += 1
            if count == ord:
                print "line: %d, %s" % (count, os.path.join(dirname, filename))
                break

query_ordinal(15879)

