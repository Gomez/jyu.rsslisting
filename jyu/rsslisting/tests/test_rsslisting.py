import unittest
from jyu.rsslisting.tests import base

from jyu.rsslisting.content.rsslisting import RSSListing

class TestContentType(base.ContentTypeTestCase):
    
    name = 'RSS Listing'
    schema = RSSListing.schema

    def test_exists(self):
        self.failUnless(self.name in self.types.objectIds())

    def test_factory(self):
        self.failUnless(self.name in self.factory.getFactoryTypes().keys())

    def test_properties(self):
        self.assertProperty('title',                 'RSS Listing')
        self.assertProperty('description',           'A page, which displays an RSS feeds (or aggregation of several feeds) in the same way as RSS portlet does')
        self.assertProperty('i18n_domain',           'jyu.rsslisting')
        self.assertProperty('content_icon',          '++resource++jyu.rsslisting.images/rsslisting_icon.gif')
        # See http://dev.plone.org/plone/ticket/8161 for
        self.assertProperty('content_meta_type',     'RSSListing')
        self.assertProperty('product',               'jyu.rsslisting')
        self.assertProperty('factory',               'addRSSListing')
        self.assertProperty('immediate_view',        'atct_edit')
        self.assertProperty('global_allow',          False)
        self.assertProperty('filter_content_types',  False)
        self.assertProperty('allowed_content_types', ())
        self.assertProperty('allow_discussion',      False)
        self.assertProperty('default_view',          'view')
        self.assertProperty('view_methods',          ('view',))

    def test_method_aliases(self):
        self.assertMethodAlias('(Default)', '(dynamic view)')
        self.assertMethodAlias('edit', 'atct_edit')
        self.assertMethodAlias('sharing', '@@sharing')
        self.assertMethodAlias('view', '(selected layout)')

    def test_actions(self):
        self.assertAction('view', {
            'title':    'View',
            'category': 'object',
            'condition_expr': '',
            'url_expr': 'string:${object_url}/view',
            'visible':  True,
            'permission': ('View',)
        })
        self.assertAction('edit', {
            'title':          'Edit',
            'category':       'object',
            'condition_expr': 'not:object/@@plone_lock_info/is_locked_for_current_user|python:True',
            'url_expr':       'string:${object_url}/edit',
            'visible':        True,
            'permission':     ('Modify portal content',)
        })

    def test_fields(self):
        self.failUnless('count' in self.fieldnames)
        self.failUnless('url' in self.fieldnames)
        self.failUnless('timeout' in self.fieldnames)

    def test_count_field(self):
        field = self.schema.get('count')
        self.assertEquals('Products.Archetypes.Field.IntegerField', field.getType())
        self.assertEquals(True, field.required)
        self.assertEquals(5, field.default)
        self.assertEquals('IntegerWidget', field.getWidgetName())

    def test_url_field(self):
        field = self.schema.get('url')
        self.assertEquals('Products.Archetypes.Field.TextField', field.getType())
        self.assertEquals(True, field.required)
#        self.assertEquals("(('isURL', V_REQUIRED))", str(field.validators))
        self.assertEquals('TextAreaWidget', field.getWidgetName())

    def test_timeout_field(self):
        field = self.schema.get('timeout')
        self.assertEquals('Products.Archetypes.Field.IntegerField', field.getType())
        self.assertEquals(True, field.required)
        self.assertEquals(100, field.default)
        self.assertEquals('IntegerWidget', field.getWidgetName())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestContentType))
    return suite
