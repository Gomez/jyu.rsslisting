from zope.interface import Interface
from zope import schema

from zope.i18nmessageid import Message as _ # requires explicit domain

class IRSSListing(Interface):
    """A content type, which displays an RSS feed in the same way as
    RSS Portlet does.
    """

    # Cloned from: plone.app.portlets.portlets.rss.IRSSPortlet
    count = schema.Int(title=_(u'Number of items to display', domain="plone"),
                       description=_(u'How many items to list.', domain="plone"),
                       required=True,
                       default=5)
    url = schema.Text(title=_(u'List of RSS feed URLs', domain="jyu.rsslisting"),
                      description=_(u'List of links to the RSS feeds to display. Please, enter only one link per line.',
                                    domain="jyu.rsslisting"),
                      required=True,
                      default=u'')
    timeout = schema.Int(title=_(u'Feed reload timeout', domain="plone"),
                         description=_(u'Time in minutes after which the feed should be reloaded.', domain="plone"),
                         required=True,
                         default=100)                        

    showMoreEnabled = schema.Bool(
        title=_(u'Show link to show more', domain="jyu.rsslisting"),
        description=_(u'When set there will be link at the end to show all the results. If there is more than one RSS feed defined, only the first RSS feed will be linked.', domain="jyu.rsslisting"),
        required = False,
        )
