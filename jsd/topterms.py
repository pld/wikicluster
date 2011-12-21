# script to parse the cluster_analyze file
# imports the top terms of a cluster to a dictionary
# cluster_terms dictionary structure:
#   cluster_id: dictionary_terms
# dictionary_terms structure:
#   term:weight

from pprint import *

top_k_cluster_terms_file = "../cluster_analyze.txt"
#	Top Terms: 
toptermsline ="\tTop Terms: \n"
file = open(top_k_cluster_terms_file,"r")

cluster_terms = dict()
cluster = 0
i = 0

_verbose = False

for line in file:
    if line.startswith("CL") or line.startswith("VL"):
        cluster += 1
        i = 0
        cluster_terms[cluster] = dict()
        if _verbose:
            print "\nCluster {0}:".format(cluster)
        pass
    elif line == toptermsline:
        pass
    else:
        words = line.split(" ")
        i += 1
        for w in words:
            if w.startswith("\t\t"):
                term = w[2:len(w)]
            elif w != "" and w != "=>":
                weight = w[0:len(w)-1]
            else:
                pass
        cluster_terms[cluster][term] = float(weight)
        if _verbose:
            print "{0}:\t{1}:{2}".format(i,term,weight)

pprint(cluster_terms)

