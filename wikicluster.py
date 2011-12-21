import sys
sys.path.append('wikilabel')
sys.path.append('jsd')
import wikiquery, wikilabel, mijudge, spjudge
import jsd
import parsetermlist
import evaluate
import util
import string
import re
from collections import defaultdict

class WikiCluster:
    # array of test term strings to search and fetch labels for
    test_term_sets = [
        ['amsterdam', 'amsterdam holland', 'amsterdam europe'],
        ['new york', 'new york city', 'york'],
    ]

    cluster_word_list = "makeclusters/top_words_lower.txt"
    baseline_term_list = "makeclusters/top_terms_lower.txt"
    num_top_terms = 20          # top reordered terms to take
    reorder_top = 20            # reorder top words
    max_search_results = 20    # 100 documents, best results in Carmel paper
    labels_to_print = 5
    label_min_length = 5
    # what to pull from Wikipedia pages
    use_anchors = False
    use_categories = True
    use_headlines = True
    # parameters
    use_spj = True
    use_jsd = True
    use_num_anchors = True
    alpha_num_plus = re.compile('[\d\W_-]+')
    label_stop_words = [
        'http',
        'html',
        'disambiguation',
        'loanwords',
        'nothing'
    ]

    def __init__(self, debug = False):
        if self.use_jsd:
            terms = jsd.JSD(self.cluster_word_list, self.reorder_top)
            term_sets = map(lambda x: list(zip(*x)[0])[0:self.num_top_terms], terms.jsd.values())
        else:
            term_sets = parsetermlist.ParseTermList(self.baseline_term_list).terms
        results = defaultdict(list)

        wl = wikilabel.WikiLabel(self.max_search_results, debug)
        num_term_sets = len(term_sets)

        for idx, terms in enumerate(term_sets):
            if debug:
                util.log("%d%%, labeling set %d/%d" % (100*float(idx+1)/num_term_sets, idx+1, num_term_sets), terms)
            wl.fetch_labels("\"" + "\" OR \"".join(terms) + "\"")
            results['docs'].append(wl.labels_for_urls.values())

            # { label => doc rank }
            labels_to_ranks = defaultdict(list)
            labels_to_num_anchors = defaultdict(list)
            # { doc rank => label }
            ranks_to_labels = dict()
            for result in results['docs'][-1]:
                rank = result.rank
                ranks_to_labels[rank] = labels = self.__labels_for_result(result, terms)
                results['candidates'].append(labels)
                for label in labels:
                    labels_to_ranks[label].append(rank)
                    labels_to_num_anchors[label].append(result.num_anchors)
            combined = self.__judge(terms, labels_to_ranks, ranks_to_labels, labels_to_num_anchors)
            results['scores'].append(combined[0])
            results['labels'].append(list(combined[1]))
            if debug:
                util.log('scores', results['scores'][-1][0:5])
                util.log('results', ", ".join(results['labels'][-1][0:5]))
            else:
                self.print_labels(results)
        self.results = results

    def eval(self):
        ev = evaluate.Evaluate(self.results['labels'])
        ev.score()
        print util.list_as_dec_str(ev.match_at_k)
        print util.list_as_dec_str(ev.mrr_at_k)

    def print_labels(self, results = None):
        if results:
            print "'" + "', '".join(results['labels'][-1][0:self.labels_to_print]) + "'"
        else:
            for labels in self.results['labels']:
                print "'" + "', '".join(labels[0:self.labels_to_print]) + "'"

    def __labels_for_result(self, result, terms):
        """
        Pull labels from results and TODO: add in terms if appearing in results
        """
        labels = list(result.title)
        if self.use_categories:
            labels += result.categories
        if self.use_anchors:
            labels += result.anchors
        if self.use_headlines:
            print result.headlines
            labels += result.headlines
        # lower case and remove non alpha numeric like
        labels = set(map(self.__process_label, set(labels)))
        # remove short labels
        labels = filter(lambda x: len(x) >= self.label_min_length, labels)
        # remove stop words
        labels = [item for item in set(labels) if not (item in self.label_stop_words or any(map(lambda x: x in item, self.label_stop_words)))]
        return self.__merge_labels(labels)

    def __merge_labels(self, labels):
        """
        Merge labels if one label is a substr of another remove longer label.  This is likely to strong in many cases.
        """
        new_labels = []
        for label in labels:
            if all(map(lambda x: re.search("\\b" + x + "\\b", label) == None, [l for l in labels if l != label])):
                new_labels.append(label)
        return new_labels

    def __process_label(self, label):
        return ' '.join(re.sub("\\b[\\w']{1,3}\\b", "", self.alpha_num_plus.sub(' ', label)).lower().split())

    def __judge(self, terms, labels_to_ranks, ranks_to_labels, labels_to_num_anchors):
        if self.use_spj:
            if self.use_num_anchors:
                spj = spjudge.SPJudge(terms, labels_to_ranks, ranks_to_labels, labels_to_num_anchors)
            else:
                spj = spjudge.SPJudge(terms, labels_to_ranks, ranks_to_labels)
            combined = zip(spj.scores, spj.labels)
        else:
            mij = mijudge.MIJudge(terms, labels_to_ranks)
            combined = zip(mij.scores, labels_to_ranks.keys())
        combined.sort()
        combined.reverse()
        return zip(*combined)

wc = WikiCluster(True)
wc.print_labels()
wc.eval()

