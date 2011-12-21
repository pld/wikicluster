from pprint import *

_normalize = False
_verbose = False

def parse_top_words(top_terms_file = None):
    if top_terms_file == None:
        top_terms_file = "../makeclusters/top_words.txt"
    file = open(top_terms_file,"r")

    cluster_terms = dict()
    cluser = 0
    i = 0

    dictionary = dict()
    # term:dict_tfs
    # dict_tfs:
    #   cluster_id:tf
    for line in file:
        if i == 0:
            i += 1
        elif i == 1:
            i += 1
        elif i == 21:
            i = 1
            words = line.split(" ")
            dictionary[words[1]] = dict()
            for j in range(2,len(words)):
                cluster_id = j-1
                tf         = words[j]
                dictionary[words[1]][cluster_id] = int(tf)
        else:
            words = line.split(" ")
            dictionary[words[1]] = dict()
            for j in range(2,len(words)):
                cluster_id = j-1
                tf         = words[j]
                dictionary[words[1]][cluster_id] = int(tf)
            i += 1
            # print words
    # normalization, is bad?
    if _normalize:
        for word, cl_to_num in dictionary.items():
            num_sum = float(sum(cl_to_num.values()))
            for cl, num in cl_to_num.items():
                cl_to_num[cl] = num / num_sum
            dictionary[word] = cl_to_num
        pprint(dictionary)
    return dictionary

def parse_cluster_analyze():
    # imports the top terms of a cluster to a dictionary
    # cluster_terms dictionary structure:
    #   cluster_id: dictionary_terms
    # dictionary_terms structure:
    #   term:weight
    top_k_cluster_terms_file = "../cluster_analyze.txt"
    #	Top Terms: 
    toptermsline ="\tTop Terms: \n"

    file = open(top_k_cluster_terms_file,"r")

    cluster_terms = dict()

    cluster = 0
    i = 0
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
                    if w.startswith("=>"):
                        weight = w[2:len(w)-1]
                    else:
                        weight = w[0:len(w)-1]
                else:
                    pass
            cluster_terms[cluster][term] = float(weight)
            if _verbose:
                print "{0}:\t{1}:{2}".format(i,term,weight)
    if _verbose:
        pprint(cluster_terms)
    return cluster_terms

