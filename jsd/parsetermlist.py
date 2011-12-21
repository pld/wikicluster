class ParseTermList:
    def __init__(self, terms_file, num_terms = 20):
        f = open(terms_file, "r")
        ret_terms = []
        group = 0
        for line in f:
            terms = line.split()
            if len(terms) < 2:
                continue
            term = terms[1]
            if term.isdigit():
                group += 1
                ret_terms.append([])
            else:
                ret_terms[group - 1].append(term)
        f.close()
        self.terms = ret_terms

