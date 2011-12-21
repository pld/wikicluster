from math import log
from pprint import *
from collections import defaultdict
from operator import itemgetter
import parsecluster

class JSD:
    def __init__(self, terms_file = None, top_limit = 20):
        # import top 1000 terms per cluster_id
        top_terms_dict = parsecluster.parse_top_words(terms_file)
        # TopN = 100
        # total terms dictionary
        q_dict = defaultdict(int)
        for term in top_terms_dict:
            # compute term weight in the collection
            for k in top_terms_dict[term]:
                q_dict[term] += top_terms_dict[term][k]
        jsd = dict()
        jsd_sorted = dict()
        for term in top_terms_dict:
            for cluster_id in top_terms_dict[term]:
                jsd_sorted[cluster_id] = []
        for term in top_terms_dict:
            for cluster_id in top_terms_dict[term]:
                jsd[cluster_id] = []
                tf = top_terms_dict[term][cluster_id]
                tuple = term, tf
                jsd_sorted[cluster_id] += [tuple]
        for term in top_terms_dict:
            for cluster_id in top_terms_dict[term]:
                jsd_sorted[cluster_id] = sorted(jsd_sorted[cluster_id], key=itemgetter(1), reverse=True)
                jsd_sorted[cluster_id] = jsd_sorted[cluster_id][0:top_limit]

        # Compute JSD per term, per cluster
        # jsd dictionary
        # structure: cluster_id:array_tuples(term,weight)
        # JSD(P|Q) = 0.5 * D(P|M) + 0.5 * D(P|Q)
        # M = 0.5 * (P + Q)
        # Q(t) = Sum(P_i(t))
        # D(P|Q) = Sum(P(i) * log(P(i) / Q(i)))
        for cluster_id in jsd_sorted:
            for term,tf in jsd_sorted[cluster_id]:
                p_t_w = top_terms_dict[term][cluster_id]
                if p_t_w > 0:
                    q_t_w = q_dict[term]
                    M     = 0.5 * (p_t_w + q_t_w)
                    if p_t_w == 0:
                        D_P_M = 0
                    else:
                        D_P_M = p_t_w * (log (p_t_w / M))
                    if M == 0:
                        D_Q_M = 0
                    else:
                        D_Q_M = q_t_w * (log (float(q_t_w) / M))
                    jsd_tw = 0.5 * D_P_M + 0.5 * D_Q_M
                    tuple = term , jsd_tw
                    jsd[cluster_id] += [tuple]
        # Sort the array of tuples by weight
        for term in top_terms_dict:
            for cluster_id in top_terms_dict[term]:
                jsd[cluster_id] = sorted(jsd[cluster_id], key=itemgetter(1), reverse=True)
        self.jsd = jsd

