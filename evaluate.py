from nltk.corpus import wordnet as wn
import re
import Stemmer

class Evaluate:
    # the 20 news groups
    # reordered
    ground_truth_labels = [
        "science.space",
        "science.medicine",
        "computer.system.mac.hardware.macintosh.apple",
        "talk.politics.guns",
        "science.electronics",
        "talk.politics.miscellaneous",
        "recreation.sport.baseball",
        "recreation.automobiles",
        "computer.os.ms.windows.miscellaneous.microsoft.operating.system",
        "rec.sport.hockey",
        "soc.religion.christian",
        "talk.religion.miscellaneous",
        "alternative.atheism",
        "computer.windows.x",
        "computer.system.ibm.pc.hardware",
        "talk.politics.middle_east",
        "recreation.motorcycles",
        "computer.graphics",
        "miscellaneous.forsale",
        "science.cryptography",
    ]
    # original order
    og_ground_truth_labels = [
        "comp.graphics",
        "comp.os.ms-windows.misc",
        "comp.sys.ibm.pc.hardware",
        "comp.sys.mac.hardware",
        "comp.windows.x",
        "rec.autos",
        "rec.motorcycles",
        "rec.sport.baseball",
        "rec.sport.hockey",
        "sci.crypt",
        "sci.electronics",
        "sci.med",
        "sci.space",
        "misc.forsale",
        "talk.politics.misc",
        "talk.politics.guns",
        "talk.politics.mideast",
        "talk.religion.misc",
        "alt.atheism",
        "soc.religion.christian"
    ]
    max_k = 5

    def __init__(self, labels = None):
        self.labels = labels
        # label is correct if it is identical, an inflection, or a Wordnet synonym of the cluster's correct label
        stemmer = Stemmer.Stemmer('english')
        # split of non alpha
        self.p_non_char = p_non_char = re.compile('[\W_]+')
        ground_truth_labels = self.ground_truth_labels
        ground_truth_labels = map(lambda x: p_non_char.split(x), ground_truth_labels)
        # add stemmed version
        ground_truth_labels = map(lambda label_set: list(set(label_set + stemmer.stemWords(label_set))), ground_truth_labels)
        # add synonyms
        new_gt_labels = []
        for labels in ground_truth_labels:
            new_labels = []
            for label in labels:
                for synset in wn.synsets(label):
                    new_labels += map(lambda x: p_non_char.split(x), synset.lemma_names)
            new_labels = [item for sublist in new_labels for item in sublist]
            new_gt_labels.append(list(set(new_labels + labels)))
        self.ground_truth_labels = new_gt_labels
        min_labels = min(map(len, labels))
        if min_labels < self.max_k:
            self.max_k = min_labels

    def test(self):
        # test candidate labels
        self.labels = [
            ["recreation", "graphics"],
            ["recreation", "misc"],
            ["recreation", "hardware"],
            ["recreation", "hardware"],
            ["recreation", "windows"],
            ["recreation", "autos"],
            ["recreation", "motorcycles"],
            ["recreation", "baseball"],
            ["recreation", "hockey"],
            ["recreation", "crypt"],
            ["recreation", "electronics"],
            ["recreation", "med"],
            ["recreation", "space"],
            ["recreation", "forsale"],
            ["recreation", "politics"],
            ["recreation", "guns"],
            ["recreation", "mideast"],
            ["recreation", "religion"],
            ["recreation", "atheism"],
            ["recreation", "christian"]
        ]
        self.max_k = 2
        self.score()

    def score(self):
        ground_truth_labels = self.ground_truth_labels
        max_k = self.max_k
        p_non_char = self.p_non_char
        # Match@K
        # Is the relative number of clusters for which at least one of the top-k labels is correct.
        match_at_k = [0]*max_k

        # MRR@K
        # Given an ordered list of k proposed labels for a cluster, the reciprocal rank is the
        # inverse of the rank of the first correct label, or zero if no label in the list is correct.
        # The mean reciprocal rank at k (MRR@K) is the average of the reciprocal ranks of all clusters.
        mrr_at_k = [0]*max_k
        for k in range(max_k):
            for idx, candidate_labels in enumerate(self.labels):
                snt = False
                for idx_cl, candidate_label in enumerate(candidate_labels[0:k+1]):
                    # we take highest score for label against any ground truth cluster labels
                    for gt_labels in ground_truth_labels:
                        for gt_label in gt_labels:
                            for term in [candidate_label] + p_non_char.split(candidate_label):
                                # print "gt: %s =? cn: %s" % (gt_label, term)
                                if gt_label.lower() == term.lower():
                                    match_at_k[k] += 1
                                    mrr_at_k[k] += 1/float(idx_cl + 1)
                                    snt = True
                                    break
                            if snt: break
                        if snt: break
                    if snt: break
        self.match_at_k = map(lambda x: float(x) / len(ground_truth_labels), match_at_k)
        self.mrr_at_k = map(lambda x: float(x) / len(ground_truth_labels), mrr_at_k)

def main()
    e = Evaluate()
    print e.ground_truth_labels
    e.test()
    print e.match_at_k
    print e.mrr_at_k

# main()

