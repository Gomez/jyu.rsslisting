RSS Listing
===========

**RSS Listing** is a content type, which displays an RSS feed in the
same way as the default **RSS Portlet** does.

.. contents::

Public resources
----------------

**RSS Listing** installs a public resource ``++resource++jyu.rsslisting.images/rsslisting_icon.gif`` for its content type icon::

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser(); portal_url = self.portal.absolute_url()
    >>> browser.open(portal_url + "/++resource++jyu.rsslisting.images/rsslisting_icon.gif")

and ``++resource++jyu.rsslisting.styles/rsslisting.css`` for its stylesheet::

    >>> browser.open(portal_url + "/++resource++jyu.rsslisting.styles/rsslisting.css")

Creating content
----------------

By default, adding **RSS Listing** is not allowed globally. Let's
allow it to make it easier to test::

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal_types = getToolByName(self.portal, "portal_types")
    >>> rss_listing = portal_types.get("RSS Listing")
    >>> rss_listing
    <DynamicViewTypeInformation at /plone/portal_types/RSS Listing>

    >>> rss_listing.global_allow = True
    >>> rss_listing.global_allow
    True

Now **RSS Listing** is addable by any *contributor*. Let's

1. open the front page::

    >>> browser.open(portal_url)

2. enter the log in details::

    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = 'secret'

3. and log in::

    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

Now we should be able to see **RSS Listing** in the *add item* menu::

    >>> browser.getLink(id='rss-listing').url.endswith("createObject?type_name=RSS+Listing")
    True

To add a single **RSS Listing**

1. click it from the *add item* menu::

    >>> browser.getLink(id='rss-listing').click()

2. enter RSS information::

    >>> browser.getControl(name='title').value = "Slashdot"
    >>> browser.getControl(name='description').value = "Yesterday's news!"
    >>> browser.getControl(name='url').value = "http://rss.slashdot.org/Slashdot/slashdot"
    >>> browser.getControl(name='count').value = "10"
    >>> browser.getControl(name='timeout').value = "100"

3. and submit the form::

    >>> browser.getControl(name='form_submit').click()

Now a new **RSS Listing** has been created::

    >>> 'slashdot' in self.portal.objectIds()
    True

Publishing content
------------------

By default, **RSS Listing** can be published by any *reviewer*. Let's

1. log out::

    >>> browser.getLink('Log out').click()

2. open the front page::

    >>> browser.open(portal_url)

3. enter the log in details::

    >>> browser.getControl(name='__ac_name').value = 'reviewer'
    >>> browser.getControl(name='__ac_password').value = 'secret'

4. and log in::

    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

To publish the **RSS Listing**

1. navigate to the content::
 
    >>> browser.open(portal_url + "/slashdot")

2. and publish it::

    >>> browser.getLink('Publish').click()

Viewing content
---------------

Published **RSS Listing** should be visible to everybody. Let's

1. log out::

    >>> browser.getLink('Log out').click()

2. navigate to the content::

    >>> browser.open("%(portal_url)s/slashdot" % vars())

**RSS Listing** is being rendered::

    >>> "Yesterday's news!" in browser.contents
    True

With required 10 feed items::

    >>> browser.contents.count("<a href=\"http://rss.slashdot.org/")
    10


