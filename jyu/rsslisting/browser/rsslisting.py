from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets.rss import FEED_DATA, Renderer
from plone.app.portlets.portlets.rss import RSSFeed as PloneRSSFeed

#from plone.app.portlets.portlets import feedparser
from DateTime import DateTime

from zLOG import LOG, INFO, ERROR

import feedparser
import htmlentitydefs
import time
import re

STRIP_TAGS_REGEXP = re.compile("<[a-zA-Z\/][^>]*>")
STRIP_WHITESPACES_REGEXP = re.compile("[\s]+")

class RSSFeed(PloneRSSFeed):
    """ Adds a few patches to the default RSSFeed """

    @staticmethod
    def unescape(text):
        """Removes HTML or XML character references and entities from a text string.
        By Fredrik Lundh: http://effbot.org/zone/re-sub.htm#unescape-html
        """
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)

    def _trim(self, text):
        text = STRIP_TAGS_REGEXP.sub('', text)
        text = STRIP_WHITESPACES_REGEXP.sub(' ', text)
        return RSSFeed.unescape(text).strip()

    # Support for Meltwater News' 'source'-tag
    def _start_source(self, attrsD):
        self.push('source', 0)

    def _end_source(self):
        value = self.pop('source')
        self.pushContent('source', value, 'text/plain', 1)

    def _retrieveFeed(self):
        """do the actual work and try to retrieve the feed"""
        # Patch #1: Add otherwise unsupported timezones
        DateTime._tzinfo._zmap.update({
            'edt': 'GMT-0400',
            'z': 'GMT-0000'
        })
        DateTime._tzinfo._zidx = DateTime._tzinfo._zmap.keys()
        #
        url = self.url
        if url!='':
            self._last_update_time_in_minutes = time.time()/60
            self._last_update_time = DateTime()
            # Path #5: Support for Meltwater News' 'source'-tag
            feedparser._FeedParserMixin._start_source = self._start_source
            feedparser._FeedParserMixin._end_source = self._end_source
            #
            d = feedparser.parse(url)
            if d.bozo==1:
                self._loaded = True # we tried at least but have a failed load
                self._failed = True
                return False
            self._title = d.feed.title
            self._siteurl = d.feed.link
            self._items = []
            for item in d['items']:
                try:
                    link = item.links[0]['href']
                    itemdict = {
                        # Patch #4: Include feed title, since we support multiple feeds
                        'source' : self._title,
                        #
                        'title' : item.title,
                        'url' : link,
                        'summary' : item.get('description',''),
                        'source' : item.get('source',''),
                    }
                    if hasattr(item, "updated"):
                        # Patch #3: Graceful failure when unsupported timezone
                        try:
                            itemdict['updated']=DateTime(item.updated)
                        except DateTime.SyntaxError:
                            LOG('jyu.rsslisting', ERROR, 'Unsupported TimeZone in "%s".' % item.updated)
                            LOG('jyu.rsslisting', INFO, 'Using the current time as RSS itemstamp.')
                            LOG('jyu.rsslisting', INFO, 'Update jyu.rsslisting.browser.rsslisting.RSSFeed._retrieveFeed.')
                            itemdict['updated']=DateTime()
                        #
                            
                except AttributeError:
                    continue
                # Patch #2: Strip HTML tags
                itemdict['source'] = self._trim(itemdict['source'])
                itemdict['title'] = self._trim(itemdict['title'])
                itemdict['summary'] = self._trim(itemdict['summary'])
                if len(itemdict['summary']) > 509: # Just some arbitrary truncation
                    itemdict['summary'] = itemdict['summary'][:510] + "..."
                #
                self._items.append(itemdict)
            self._loaded = True
            self._failed = False
            return True
        self._loaded = True
        self._failed = True # no url set means failed 
        return False # no url set, although that actually should not really happen

class RSSListingView(BrowserView, Renderer):
    """ Adds support for RSSListing template """

    __call__ = ViewPageTemplateFile('rsslisting_view.pt')
    # ``render_full`` provides support for Renderer's ``self.render()``
    # ``rsslisting`` is required by ``portalviewbox.pt``
    template = ViewPageTemplateFile('rsslisting_view.pt')
    render_full = ViewPageTemplateFile('rsslisting_boxview.pt')
    
    def __init__(self, context, request):
        """ Sets up a few convenience object attributes """
        self.context = context
        self.request = request
        # Sets ${template/id}
        self.__call__.id = "rss-listing"
        # Sets self.data, which is required by Renderer
        self.data = context
        # Updates feed if needed
        self.update()

    def getURLs(self):
        return self.data.url.strip().replace("\r", '').split("\n") ;

    def _getFeed(self, url=None):
        """return a feed object but do not update it"""
        url = url or self.getURLs()[0]
        feed = FEED_DATA.get(url,None)
        if feed is None:
            # create it
            feed = FEED_DATA[url] = RSSFeed(url,self.data.timeout)
        return feed

    def _getFeeds(self):
        """return a feed object but do not update it"""
        urls = self.getURLs()
        feeds = [self._getFeed(url) for url in urls]
        return feeds

    def deferred_update(self):
        """refresh data for serving via KSS"""
        for feed in self._getFeeds():
            feed.update()

    @staticmethod
    def cmp_item(x, y):
        """ compares items by their update datetime """
        if x.has_key('updated') and y.has_key('updated'):
            return x['updated'] < y['updated'] and 1 or x['updated'] > y['updated'] and -1 or 0
        elif x.has_key('updated') and not y.has_key('updated'):
            return -1
        elif not x.has_key('updated') and y.has_key('updated'):
            return 1
        else:
            return 0

    @property            
    def items(self):
        items = []
        for feed in self._getFeeds():
            items.extend(feed.items)
        items.sort(RSSListingView.cmp_item)
        return items[:self.data.count]

    @property
    def feedAvailable(self):
        """checks if the feed data is available"""
        for feed in self._getFeeds():
            if feed.ok:
                return True
        return False

    @property    
    def feedlink(self):
        """return rss url of feed for portlet"""
        return self.getURLs()[0]

    @property    
    def showMoreEnabled(self):
        """should link to show more be enabled"""
        return self.context.getShowMoreEnabled()

class RSSListingBoxView(RSSListingView):
    """ Adds support for Portal View """
    # ``rsslisting`` is required by ``portalviewbox.pt``
    rsslisting_view = ViewPageTemplateFile('rsslisting_view.pt')
    __call__ = ViewPageTemplateFile('rsslisting_boxview.pt')
