import util
import wikiquery
import urllib2
import libxml2dom

class WikiLabel:
    def __init__(self, max_docs = 5, debug = False):
        self.max_docs = max_docs
        self.debug = debug
        self.labels_for_urls = dict()
        self.wq = wikiquery.WikiQuery()

    def fetch_labels(self, query):
        self.__clear_labels()
        self.wq.search(query, sites='en.wikipedia.org', count=self.max_docs)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'MwClient-0.6.4')]
        for idx, url in enumerate(self.wq.urls()[0:self.max_docs]):
            try:
                infile = opener.open(url)
                page = infile.read()
                doc = libxml2dom.parseString(page, html=1)
                if self.debug:
                    util.log("url", url)
                labels = DocLabels()
                labels.title = self.__collect_text(doc.xpath("//*[@id='firstHeading']")[0])
                labels.categories = self.__nodes_to_array(doc.xpath("//*[@id='mw-normal-catlinks']/span"))
                # remove disambiguation pages
                dp_str = 'Disambiguation pages'
                if dp_str in labels.categories:
                    labels.categories.remove(dp_str)
                # headline text
                labels.headlines = []
                for node in doc.xpath("//h3/*[@class='mw-headline']"):
                    labels.headlines.append(self.__collect_text(node))
                labels.num_anchors = len(doc.getElementsByTagName("a"))
                labels.anchors = []
                # only taking external link texts
                for node in doc.xpath("//ul/li/*[@class='external text']"):
                    labels.anchors.append(self.__collect_text(node))
                labels.rank = idx + 1
                self.labels_for_urls[url] = labels
            except (urllib2.HTTPError, IndexError), e:
                if self.debug:
                    util.error("%s, url: %s" % (e, url))

    def __collect_text(self, node):
        """A function which collects text inside 'node', returning that text."""
        s = ""
        for child_node in node.childNodes:
            if child_node.nodeType == child_node.TEXT_NODE:
                s += child_node.nodeValue
            else:
                s += self.__collect_text(child_node)
        return s

    def __nodes_to_array(self, nodes):
        return reduce(lambda x, y: x + [self.__collect_text(y)], nodes, [])

    def __clear_labels(self):
        self.labels_for_urls = dict()

class DocLabels:
    pass

