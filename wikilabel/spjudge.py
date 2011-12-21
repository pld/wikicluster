import math
from collections import defaultdict
import abstractjudge

class SPJudge(abstractjudge.AbstractJudge):
    def store_scores(self, labels_to_ranks):
        label_scores = map(self.__score_one_label, labels_to_ranks.values(), self.labels_to_num_anchors and
            self.labels_to_num_anchors.values())
        self.labels = labels = labels_to_ranks.keys()
        label_to_scores = dict()
        kws_to_labels = defaultdict(set)
        for idx, label in enumerate(labels):
            label_to_scores[label] = label_scores[idx]
            for kw in set(label.split()):
                kws_to_labels[kw].add(label)
        self.kws_to_labels = kws_to_labels
        self.label_to_scores = label_to_scores
        kw_scores = map(self.__score_one_kw, kws_to_labels.keys())
        scores = []
        for label in labels:
            kws = set(label.split())
            scores.append(reduce(lambda x,y: x + kw_scores[kws_to_labels.keys().index(y)], kws, 0)/len(kws))
        return scores

    def __score_one_label(self, ranks, num_anchors):
        """
        scores each candidate label with respect to the scores of the documents
        in the result set associated with that label.
        """
        total = 0
        if self.labels_to_num_anchors:
            # num_anchors = 
            for i, rank in enumerate(ranks):
                total += (math.log(num_anchors[i]) + 1 / float(rank)) / len(self.ranks_to_labels[rank])
        else:
            total = reduce(lambda x,y: x + (1/float(y))/len(self.ranks_to_labels[y]), ranks, 0)
        return total

    def __score_one_kw(self, kw):
        return reduce(lambda x,y: x + self.label_to_scores[y], self.kws_to_labels[kw], 0)/len(self.kws_to_labels[kw])

