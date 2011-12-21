import bossapi

class WikiQuery:
    appid = "[ENTER YOUR APP ID HERE]"

    def __init__(self):
        # declare Yahoo! BOSS searcher
        self.searcher = bossapi.Boss(self.appid)

    def search(self, query, **kwargs):
        # search yahoo
        self.results = self.searcher.do_web_search(query, **kwargs)

    def urls(self):
        # pull out URLs
        urls = [result['url'] for result in self.results['ysearchresponse']['resultset_web']]
        return urls

    def total_hits(self):
        return int(self.results['ysearchresponse']['totalhits'])

