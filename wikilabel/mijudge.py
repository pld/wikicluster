import abstractjudge

class MIJudge(abstractjudge.AbstractJudge):
    def store_scores(self, labels_to_ranks):
        labels = labels_to_ranks.keys()
        return reduce(lambda x, y: x + [self.score_one_label(y)], labels, [])

    def score_one_label(self, label):
        """mutual information between label and terms"""
        self.progress += 1
        print "%d percent" % (100 * self.progress / float(len(self.labels)))
        return reduce(lambda x, y: x + self.score_one_label_and_term(label, y), self.terms, 0)

    def score_one_label_and_term(self, label, term):
        """
        Pointwise mutual information between two words.
        Get external counts as number of web search hits.
        """
        wq = self.wq
        label_term = label + " " + term
        pr_label_term = self.term_to_hits.get(label_term)
        if not pr_label_term:
            wq.search(label_term)
            pr_label_term = self.term_to_hits[label_term] = float(wq.total_hits())
        pr_label = self.term_to_hits.get(label)
        if not pr_label:
            wq.search(label)
            pr_label = self.term_to_hits[label] = wq.total_hits()
        pr_term = self.term_to_hits.get(term)
        if not pr_term:
            wq.search(term)
            pr_term = self.term_to_hits[term] = wq.total_hits()
        return abstractjudge.log(pr_label_term / (pr_label * pr_term))

