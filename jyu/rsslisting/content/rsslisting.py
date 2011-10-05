"""Definition of the RSSListing content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from jyu.rsslisting.interfaces.rsslisting import IRSSListing
from jyu.rsslisting.config import PROJECTNAME

from zope.i18nmessageid import Message as _ # requires explicit domain

RSSListingSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.IntegerField('count',
        required=True,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(label=_(u'Number of items to display', domain="plone"),
                                   description=_(u'How many items to list.', domain="plone")),
        default=5,
        ),

    atapi.TextField('url',
        required=True,
        searchable=True,
#        validators=(('isURL'),),
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(label=_(u'List of RSS feed URLs', domain="jyu.rsslisting"),
                                    description=_(u'List of links to the RSS feeds to display. Please, enter only one link per line.',
                                                  domain="jyu.rsslisting")),
        ),

    atapi.IntegerField('timeout',
        required=True,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(label=_(u'Feed reload timeout', domain="plone"),
                                   description=_(u'Time in minutes after which the feed should be reloaded.', domain="plone")),
        default=100,
        ),

    atapi.BooleanField('showMoreEnabled',
        required = False,
        storage = atapi.AnnotationStorage(),
        widget = atapi.BooleanWidget(
            label = _(u'Show link to show more', domain="jyu.rsslisting"),
            description = _(u'When set there will be link at the end to show all the results. If there is more than one RSS feed defined, only the first RSS feed will be linked.', domain="jyu.rsslisting"),
            )
        ),
    ))


RSSListingSchema['title'].storage = atapi.AnnotationStorage()
RSSListingSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(RSSListingSchema, folderish=False, moveDiscussion=False)

class RSSListing(base.ATCTContent):
    """Describe an RSSListing.
    """
    implements(IRSSListing)
    
    portal_type = "RSS Listing"
    _at_rename_after_creation = True
    schema = RSSListingSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    count = atapi.ATFieldProperty('count')
    url = atapi.ATFieldProperty('url')
    timeout = atapi.ATFieldProperty('timeout')

    showMoreEnabled = atapi.ATFieldProperty('showMoreEnabled')

    def getText(self):
        view = self.restrictedTraverse('view')
        return view.render()

atapi.registerType(RSSListing, PROJECTNAME)
