import wikiquery
from math import log

class AbstractJudge:
    term_to_hits = dict()
    progress = 0

    def __init__(self, terms, labels_to_ranks, ranks_to_labels = None, labels_to_num_anchors = None):
        self.labels_to_ranks = labels_to_ranks
        self.labels_to_num_anchors = labels_to_num_anchors
        self.terms = terms
        self.ranks_to_labels = ranks_to_labels
        self.wq = wikiquery.WikiQuery()
        self.scores = self.store_scores(labels_to_ranks)

