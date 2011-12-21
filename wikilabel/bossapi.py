import logging
import urllib, urllib2

try:
    import json
except ImportError:
    import simplejson as json

class Boss(object):
    def __init__(self, appid, loglevel=logging.INFO):
        self.appid = appid
        self.log_filename = 'log.log'
        logging.basicConfig(level=loglevel,
                          format='%(asctime)s %(name)-6s %(levelname)-8s %(message)s',
                          filename=self.log_filename)

    def talk_to_yahoo(self, type_, query, **kwargs):
        query = urllib.quote_plus(query)
        logging.info('Query:%s'%query)
        logging.info('type_:%s'%type_)
        logging.info('Other Args:%s'%kwargs)
        base_url = 'http://boss.yahooapis.com/ysearch/%s/v1/%s?%s'
        kwargs['appid'] = self.appid
        payload = urllib.urlencode(kwargs)
        final_url = base_url%(type_, query, payload)
        logging.info('final_url: %s'%final_url)
        response=urllib.urlopen(final_url)
        data=json.load(response)
        logging.info('data:%s'%data)
        return data

    def do_web_search(self, query, **kwargs):
        return self.talk_to_yahoo('web', query, **kwargs)

    def do_news_search(self, query, **kwargs):
        return self.talk_to_yahoo('news', query, **kwargs)

    def do_spelling_search(self, query, **kwargs):
        return self.talk_to_yahoo('spelling', query, **kwargs)

    def do_images_search(self, query, **kwargs):
        return self.talk_to_yahoo('images', query, **kwargs)

    def do_siteexplorer_search(self, query, **kwargs):
        return self.talk_to_yahoo('se_inlink', query, **kwargs)

